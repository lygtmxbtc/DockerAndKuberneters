# Replication Controller
## edit yaml
```bash
vim first-rc.yaml
```
```yaml
apiVersion: v1
kind: ReplicationController
metadata:
   name: my-first-rc
   labels: 
     name: my-first-controller
spec:
  replicas: 1
  selector:
     name: my-first-rc-pod
  template: 
    metadata:
     labels:
       name: my-first-rc-pod
    spec:
      containers:
      - name: my-first-rc-pod-name
        image: pytest:0.1
        command: ["/root/test_server.py"]
        ports:
        - containerPort: 7086

```
## create rc with kubectl
```bash
kubectl create -f first-rc.yaml
kubectl get rc

```

## example:
```yaml
apiVersion: v1
kind: ReplicationController
metadata:
   name: test-tcp
   labels: 
     name: test-tcp-controller
spec:
  replicas: 1
  selector:
     name: test-tcp-rc
  template: 
    metadata:
     labels:
       name: test-tcp-rc
    spec:
      containers:
      - name: test-tcp-1
        image: 172.12.78.69:5000/test-tcp-server:0.1
        command: ["/opt/tcp_server.py"]
        ports:
        - containerPort: 23333
      - name: test-tcp-1
        image: 172.12.78.69:5000/test-tcp-server:0.2
        command: ["/opt/tcp_server.py"]
        ports:
        - containerPort: 8888

```
```yaml
apiVersion: v1
kind: Service
metadata:
  name: test-tcp-service
  labels:
    name: test-tcp-service-label
spec:
  type: NodePort
  ports:
  - port: 8091
    targetPort: 23333
    protocol: TCP
  - port: 8092
    targetPort: 8888
    protocol: TCP
  selector:
    name: test-tcp-rc

```