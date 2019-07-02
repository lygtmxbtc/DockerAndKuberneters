## spark-master-deployment.yaml
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
   name: spark-master-deployment
spec:
  replicas: 1
  template:
    metadata:
     labels:
       name: spark-master-label
    spec:
      containers:
      - name: spark-master-container
        image: 172.12.78.69:5000/spark:centos.1
        imagePullPolicy: Always
        workingDir: "/root"
        command: ["/opt/spark-2.4.0-bin-hadoop2.7/sbin/start-master.sh"]
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

## spark-master-svc.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: spark-master-service
  labels:
    name: spark-master-service-label
spec:
  type: NodePort
  ports:
  - port: 17077
    targetPort: 7077
    nodePort: 30077
    name: master-node-port
    protocol: TCP
  - port: 18080
    targetPort: 8080
    nodePort: 30080
    name: master-webui-node-port
    protocol: TCP
  selector:
    name: spark-master-label
```

## spark-slave-deployment.yaml
```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
   name: spark-slave-deployment
spec:
  replicas: 2
  template:
    metadata:
     labels:
       name: spark-slave-label
    spec:
      containers:
      - name: spark-slave-container
        image: 172.12.78.69:5000/spark:centos.1
        imagePullPolicy: Always
        workingDir: "/root"
        command: ["/opt/spark-2.4.0-bin-hadoop2.7/sbin/start-slave.sh", "spark://spark-master-service:17077"]
        ports:
        - containerPort: 8081
          name: slave-ui-port
          protocol: TCP
        env:
        - name: SPARK_NO_DAEMONIZE
          value: ok
```