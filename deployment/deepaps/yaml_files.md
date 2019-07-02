# deploy deepaps with usms + redis + psql
## deepaps-rc.yaml
```yaml
apiVersion: v1
kind: ReplicationController
metadata:
   name: deepaps-sys
   labels:
     name: deepaps-sys-controller
spec:
  replicas: 1
  selector:
     name: deepaps-label
  template:
    metadata:
     labels:
       name: deepaps-label
    spec:
      containers:
      - name: usms
        image: 172.12.78.69:5000/img-usms:0.1
        imagePullPolicy: Always
        workingDir: "/root/backend"
        command: ["python3", "usms.py"]
        ports:
        - containerPort: 5055
      - name: deepaps-backend
        image: 172.12.78.69:5000/img-deepaps:0.2
        imagePullPolicy: Always
        workingDir: "/root/backend"
        command: ["python3", "deepaps.py"]
        ports:
        - containerPort: 5080
      - name: deepaps-weixin-backend
        image: 172.12.78.69:5000/img-deepaps:0.2
        imagePullPolicy: Always
        workingDir: "/root/backend"
        command: ["python3", "deepaps_weixin.py"]
        ports:
        - containerPort: 5081
      - name: deepaps-redis
        image: 172.12.78.69:5000/img-redis:0.2
        command: ["/usr/bin/redis-server", "/etc/redis/redis.conf"]
        ports:
        - containerPort: 6379

```
## deepaps-svc.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: deepaps-sys-service
  labels:
    name: deepaps-sys-service-label
spec:
  type: NodePort
  ports:
  - port: 15080
    targetPort: 5080
    nodePort: 30580
    name: deepaps-port
    protocol: TCP
  - port: 15081
    targetPort: 5081
    nodePort: 30581
    name: deepaps-weixin-port
    protocol: TCP
  selector:
    name: deepaps-label

```
## deepaps-db-svc.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: deepaps-db
spec:
  ports:
  - port: 5432
    targetPort: 5432
    protocol: TCP

```
## deepaps-db-ep.yaml
```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: deepaps-db
subsets:
  - addresses:
      - ip: 172.12.78.2
    ports:
      - port: 5432

```