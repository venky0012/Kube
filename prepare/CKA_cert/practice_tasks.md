# CKA Practice Tasks

## Environment
- Set up a local cluster using Minikube or KIND.
- Confirm `kubectl` access and cluster status.

## Basic Tasks
- Create a Pod from YAML and verify it runs.
- Create a Deployment and scale replicas.
- Expose a Deployment with a Service.

## Advanced Tasks
- Create a StatefulSet with persistent storage.
- Create a Job and a CronJob.
- Configure a DaemonSet and verify on all nodes.
- Apply node labels and schedule a pod using node affinity.
- Add a taint to a node and create a toleration.

## Networking Tasks
- Create a ClusterIP and NodePort Service.
- Configure an Ingress resource.
- Apply a NetworkPolicy to restrict traffic.

## Storage Tasks
- Create a PersistentVolume and PersistentVolumeClaim.
- Mount the PVC in a Pod.
- Use a StorageClass for dynamic provisioning.

## Security Tasks
- Create RBAC roles and role bindings for a namespace.
- Create a ServiceAccount and assign it to a Pod.
- Store sensitive data in a Secret and use it in a Pod.

## Troubleshooting Tasks
- Simulate a failing pod and troubleshoot with `kubectl describe` and `logs`.
- Diagnose node NotReady conditions.
- Find and fix resource limit issues in pods.
