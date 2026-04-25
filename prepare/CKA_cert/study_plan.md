# CKA Study Plan

## Week 1: Fundamentals and Setup
- Install Minikube or KIND for practice clusters.
- Review Kubernetes architecture: control plane, nodes, etcd, kubelet, kube-proxy.
- Learn `kubectl` basics and object configuration.
- Practice YAML manifests for Pods, Deployments, Services.

## Week 2: Workloads and Scheduling
- Study Deployments, ReplicaSets, DaemonSets, StatefulSets, Jobs, and CronJobs.
- Practice rolling updates, rollbacks, and pod lifecycle.
- Learn node labels, taints, tolerations, and affinity rules.
- Practice `kubectl explain`, `kubectl describe`, and logs.

## Week 3: Services, Networking, and Storage
- Learn Service types: ClusterIP, NodePort, LoadBalancer, and Ingress.
- Practice DNS, network policies, and service discovery.
- Study PersistentVolumes, PersistentVolumeClaims, StorageClasses.
- Practice mounting storage in Pods and resizing PVCs.

## Week 4: Security, Cluster Maintenance, Troubleshooting
- Study RBAC, ServiceAccounts, Roles, and RoleBindings.
- Learn secrets, configmaps, and security contexts.
- Practice cluster upgrades, backups, and node maintenance.
- Use troubleshooting tools: `kubectl get events`, `describe`, `logs`, `exec`, `top`.

## Exam Prep Techniques
- Timebox practice labs (70% of prep time).
- Use official Kubernetes documentation during practice.
- Review sample exam tasks and time yourself.
- Repeat weak domains until confident.
