# Basic Minikube Familiarization: Juggling Your First Clusters

Welcome to the circus of Kubernetes! In this guide, we'll "juggle" basic Minikube operations to get you comfortable with the environment. Think of Minikube as your personal Kubernetes playground – small but mighty. We'll start simple and build up to handling multiple "balls" (pods, deployments) in the air.

## Prerequisites
- Minikube installed (use our setup scripts!)
- kubectl installed
- Basic terminal knowledge

## Act 1: Starting the Show (Minikube Basics)

### 1. Start Your Minikube Cluster
```bash
minikube start --driver=docker
```
*Why?* This fires up a single-node Kubernetes cluster in a VM or container. The `--driver=docker` uses Docker as the runtime.

*Real Kubernetes note:* In production, you won't use Minikube. Real Kubernetes runs on multiple nodes in a cluster, often provisioned on cloud providers or on metal servers. You use kubeadm, managed services like EKS/GKE/AKS, or Kubernetes distributions to install it, and you interact with it the same way using `kubectl`.

*Troubleshooting note:* If `minikube start` fails because the control plane cannot connect or kubelet fails, the fix is to delete the broken cluster and restart it cleanly. The exact recovery steps we used are:

```bash
minikube delete
minikube start --driver=docker
```

This guide now explains the recovery path, and the setup scripts include a retry path that will delete and recreate the cluster if the first start attempt fails.

### 2. Check the Status
```bash
minikube status
kubectl cluster-info
```
*Juggling Tip:* Always check if your cluster is running before throwing pods around!

### 3. View Nodes
```bash
kubectl get nodes
```
*Imagination:* Your cluster is like a unicycle – one wheel (node) to balance everything on.

## Act 2: First Ball in the Air (Simple Pod)

### 4. Deploy a Simple Nginx Pod
```bash
kubectl run nginx-pod --image=nginx --port=80
```

### 5. Check Your Pod
```bash
kubectl get pods
kubectl describe pod nginx-pod
```

### 6. Expose the Pod
```bash
kubectl expose pod nginx-pod --type=NodePort --port=80
minikube service nginx-pod --url
```
*Juggling Tip:* Exposing services is like adding strings to your juggling balls – now you can access them externally!

## Act 3: Adding More Balls (Multiple Deployments)

### 7. Create a Deployment (More Stable than Pods)
```bash
kubectl create deployment hello-world --image=k8s.gcr.io/echoserver:1.4 --replicas=2
```

### 8. Scale It Up
```bash
kubectl scale deployment hello-world --replicas=4
kubectl get pods
```
*Imagination:* Scaling is like adding more balls to your juggling routine. Can you handle 4?

### 9. Expose the Deployment
```bash
kubectl expose deployment hello-world --type=NodePort --port=8080
minikube service hello-world --url
```

## Act 4: The Grand Finale (Cleanup and Advanced Tricks)

### 10. View All Resources
```bash
kubectl get all
```

### 11. Delete Resources
```bash
kubectl delete service nginx-pod
kubectl delete deployment hello-world
kubectl delete pod nginx-pod
```

### 12. Stop Minikube
```bash
minikube stop
```

## Juggling Challenges (Exercises)

1. **Beginner:** Start Minikube, deploy 3 different pods (nginx, busybox, alpine), expose them, and access via browser.

2. **Intermediate:** Create a deployment with 5 replicas, scale to 10, then back to 2. Time yourself!

3. **Advanced:** Use `kubectl run` to create pods with different resource limits. Juggle CPU and memory constraints.

4. **Circus Trick:** Deploy a pod that runs a simple web server (use `kubectl run web --image=httpd --port=80`), then update the image to a newer version without downtime.

## Pro Tips
- Use `minikube dashboard` to open the Kubernetes dashboard in your browser.
- `kubectl logs <pod-name>` to see what's happening inside.
- `kubectl exec -it <pod-name> -- /bin/bash` to "enter" the pod.
- If stuck, `minikube delete` and start fresh.

## Next Steps
Once comfortable, move to the CKA_cert materials for deeper dives. Remember, in Kubernetes, practice makes perfect – keep juggling!

*Remember:* Minikube is your training ground. The real circus is production clusters!</content>
<parameter name="filePath">/home/venkat/scripts/prepare/basic/basic_minikube_juggling.md