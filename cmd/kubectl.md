# kubectl
## config
```bash
kubectl config set-cluster k8s-cluster1 --server=http://localhost:9090
kubectl config set-context kube-system-ctx --cluster=k8s-cluster1
kubectl config use-context kube-system-ctx
kubectl config view

```
## resource
### Usage:
- resource can be used: node/pod/rc/svc/ep
- ps: node == nodes, pod == pods, svc == service == services, ep == endpoints
```text
kubectl get <resource name>         # simplified info 
kubectl describe <resource name>    # detail info

```
### Examples:
#### Node
```bash
kubectl get nodes
kubectl get nodes -o json
kubectl get nodes -o wide
```
- rest API
```bash
curl -X GET localhost:8080/api/v1/nodes
```
#### Pod
```bash
kubectl get pods
kubectl get pods --selector name=firstApp
kubectl get pod -o wide  # 查看运行中pod
kubectl describe pods
kubectl create -f ./first-pod.yaml  # 仅创建
kubectl delete -f ./first-pod.yaml  # delete
kubectl apply -f ./first-pod.yaml  # 有则修改，无则创建
# kubectl create -f ./first-pod.yaml --edit -o json

```
- rest API
```bash
curl -X GET localhost:8080/api/v1/namespaces/default/pods
```
