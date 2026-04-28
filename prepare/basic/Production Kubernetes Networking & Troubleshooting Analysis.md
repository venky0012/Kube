# **Production Kubernetes Networking: Deep Dive & Troubleshooting**

**Overview:** This document summarizes the transition from troubleshooting a Minikube multi-node cluster to understanding how these same issues manifest in "Actual" (Production-grade) Kubernetes clusters.

## ---

**1\. The Core Infrastructure Handshake**

In a production cluster (built with kubeadm or on bare-metal), nodes do not automatically become "Ready." They stay in a **NotReady** state until the **Container Network Interface (CNI)** is successfully initialized.

### **The "NotReady" Root Cause**

The Kubelet on a worker node acts as a watchdog. It checks for a network configuration file in /etc/cni/net.d/. If this file is missing or uninitialized, the node refuses to accept pods.  
**Common Production Error:**  
NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized

## ---

**2\. Common Production Misconfigurations**

| Misconfiguration | Technical Root Cause | Impact   |
| :---- | :---- | :---- |
| **Missing CNI Manifest** | kubeadm join was successful, but no network plugin (Calico/Flannel/Cilium) was applied. | Nodes remain NotReady forever. |
| **Port Blockage** | Cloud Security Groups or local firewalls block CNI traffic (e.g., UDP 8472 for VXLAN). | Nodes are Ready, but Pod-to-Pod communication fails across nodes. |
| **Cgroup Driver Mismatch** | Kubelet is set to systemd while the Container Runtime (containerd/Docker) is set to cgroupfs. | Kubelet crashes repeatedly or fails to register. |
| **MTU Mismatch** | CNI overhead (encapsulation) makes packets larger than the physical network's MTU (typically 1500). | Small pings work, but large data transfers or API calls hang. |

## ---

**3\. Deployment Types: DaemonSets vs. Deployments**

In production, system components and user applications are managed differently to ensure cluster stability.

* **DaemonSet (The System Layer):** Used for CNIs (like Flannel) and Log Collectors. It ensures that **exactly one pod** runs on every node. If you add 10 more nodes to your production cluster, the DaemonSet automatically scales the network to them.  
* **Deployment (The Application Layer):** Used for your microservices. It manages a **replica count**. If you have 3 replicas on a 10-node cluster, Kubernetes will only use 3 nodes.

## ---

**4\. Production Troubleshooting Command Reference**

### **A. Diagnosing Node Readiness**

`# Check node conditions for Pressure or Network errors`  
`kubectl describe node <node-name>`

`# View live Kubelet logs (The first place to look in production)`  
`sudo journalctl -u kubelet -f`

### **B. Diagnosing the Container Runtime**

`# Check if the runtime is actually running`  
`sudo systemctl status containerd`

`# List images pulled by the runtime (to check for pull errors)`  
`sudo crictl images`

### **C. Diagnosing CNI Health**

`# List all networking pods in the system namespace`  
`kubectl get pods -n kube-system -o wide`

`# Check the local CNI configuration on the server`  
`ls -l /etc/cni/net.d/`

`# View logs of a specific CNI pod on a specific node`  
`kubectl logs -n kube-system <cni-pod-name>`

## ---

**5\. Summary of the "Actual K8s" Workflow**

1. **Initialize Master:** kubeadm init  
2. **Install CNI (Critical Step):** kubectl apply \-f \<cni-manifest-url\>  
3. **Join Nodes:** kubeadm join ...  
4. **Verify:** kubectl get nodes (Wait for **Ready**)  
5. **Deploy App:** kubectl apply \-f \<app-deployment-url\>