## spark232-master-deployment.yaml
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
   name: spark232-master-deployment
spec:
  replicas: 1
  template:
    metadata:
     labels:
       name: spark232-master-label
    spec:
      containers:
      - name: spark232-master-container
        image: 172.12.78.69:5000/spark:centos.4
        workingDir: "/root"
        command: ["/opt/spark-2.3.2-bin-hadoop2.7/sbin/start-master.sh"]
        ports:
        - containerPort: 7077
          name: master-port
          protocol: TCP
        - containerPort: 8080
          name: master-ui-port
          protocol: TCP
        env:
        - name: SPARK_NO_DAEMONIZE
          value: ok
```

## spark232-master-svc.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: spark232-master-service
  labels:
    name: spark232-master-service-label
spec:
  type: NodePort
  ports:
  - port: 17377
    targetPort: 7077
    nodePort: 30377
    name: master-node-port
    protocol: TCP
  - port: 18380
    targetPort: 8080
    nodePort: 30380
    name: master-webui-node-port
    protocol: TCP
  selector:
    name: spark232-master-label
```

## spark232-slave-deployment.yaml
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
   name: spark232-slave-deployment
spec:
  replicas: 3
  template:
    metadata:
     labels:
       name: spark232-slave-label
    spec:
      containers:
      - name: spark232-slave-container
        image: 172.12.78.69:5000/spark:centos.4
        workingDir: "/root"
        command: ["/opt/spark-2.3.2-bin-hadoop2.7/sbin/start-slave.sh", "spark://spark232-master-service:17377"]
        ports:
        - containerPort: 8081
          name: slave-ui-port
          protocol: TCP
        env:
        - name: SPARK_NO_DAEMONIZE
          value: ok
```