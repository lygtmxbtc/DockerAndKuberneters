# 1. Dashboard (new version for k8s 1.12)
## 1.1 Create admin and bind role
### admin-user.yaml
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kube-system
```
### admin-user-role-binding.yaml
```yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system
```
## 1.2 Get admin token
```bash
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')

```
## 1.3 Generate p12
```bash
# 生成client-certificate-data
grep 'client-certificate-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d >> kubecfg.crt
# 生成client-key-data
grep 'client-key-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d >> kubecfg.key
# 生成p12
openssl pkcs12 -export -clcerts -inkey kubecfg.key -in kubecfg.crt -out kubecfg.p12 -name "kubernetes-client"
```

# 2. Dashboard (old version for k8s 1.5)
## conf 1
### rc
```bash
vim kube-ui-rc.yaml
```
```yaml
kind: ReplicationController
apiVersion: v1
metadata:
  labels:
    app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kube-system
spec:
  replicas: 1
  selector:
    app: kubernetes-dashboard
  template:
    metadata:
      labels:
        app: kubernetes-dashboard
    spec:
      containers:
      - name: kubernetes-dashboard
        image: docker.gaoxiaobang.com/kubernetes/kube-ui:v5
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
```
### service
```bash
vim kube-ui-svc.yaml
```
```yaml
kind: Service
apiVersion: v1
metadata:
  labels:
    app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kube-system
spec:
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: kubernetes-dashboard
```
## conf 2: Invalid!!!
### rc
```yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: kube-ui-v5
  namespace: kube-system
  labels:
    k8s-app: kube-ui
    version: v5
    kubernetes.io/cluster-service: "true"
spec:
  replicas: 1
  selector:
    k8s-app: kube-ui
    version: v5
  template:
    metadata:
      labels:
        k8s-app: kube-ui
        version: v5
        kubernetes.io/cluster-service: "true"
    spec:
      containers:
      - name: kube-ui
        image: docker.gaoxiaobang.com/kubernetes/kube-ui:v5
        resources:
          limits:
            cpu: 100m
            memory: 50Mi
          requests:
            cpu: 100m
            memory: 50Mi
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /
            port: 8080
          initialDelaySeconds: 30
          timeoutSeconds: 5
```
### svc
```yaml
apiVersion: v1
kind: Service
metadata:
  name: kube-ui
  namespace: kube-system
  labels:
    k8s-app: kube-ui
    kubernetes.io/cluster-service: "true"
    kubernetes.io/name: "KubeUI"
spec:
  selector:
    k8s-app: kube-ui
  ports:
  - port: 80
    targetPort: 8080
```