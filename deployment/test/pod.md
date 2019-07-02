# Pod
## edit yaml
```bash
vim first-pod.yaml
```
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: first-pod
  labels:
    name: firstApp
spec:
  containers:
  - name: python_test_server
    image: pytest:0.1
    command: ["/root/test_server.py"]
    ports:
    - containerPort: 8888

```
## create pod with kubectl
```bash
kubectl create -f first-pod.yaml
kubectl describe pod
```