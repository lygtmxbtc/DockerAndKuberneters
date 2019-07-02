# Service
## case 1
### edit service
- If you can not access nodePort outside host, run "iptables -P FORWARD ACCEPT" at this host
- targetPort == containerPort
- create service with this kind of yaml will also create endpoint
- use "kubectl create -f xxx.yaml" as usual
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-first-service
  labels:
    name: my-first-service-label
spec:
  type: NodePort
  ports:
  - port: 8086
    targetPort: 7086
    protocol: TCP
    nodePort: 30001
  selector:
    name: my-first-rc-pod

```
## case 2
### edit service
```bash
vim first-service.yaml
```
```yaml
apiVersion: v1
kind: Service
metadata:
  name: deepaps
spec:
  ports:
  - port: 5080
    targetPort: 5080
    protocol: TCP

```
### edit endpoint
```bash
vim first-endpoint.yaml
```
```yaml
apiVersion: v1
kind: Endpoints
metadata: 
  name: deepaps
subsets:
  - addresses:
      - ip: 172.12.78.75
    ports:  
      - port: 5080
```
### create
```bash
kubectl create -f first-service.yaml -f first-endpoint.yaml
```
## case 2.1
### edit service
```bash
vim first-service.yaml
```
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
### edit endpoint
```bash
vim first-endpoint.yaml
```
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
### create
```bash
kubectl create -f first-service.yaml -f first-endpoint.yaml
```