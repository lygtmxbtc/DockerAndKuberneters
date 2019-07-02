```bash
javac py_wrapper/PythonWrapper.java
jar -cef py_wrapper.PythonWrapper PythonWrapper.jar py_wrapper

```

```bash
./spark-submit --master k8s://https://172.12.78.31:6443 \
--deploy-mode cluster \
--name spark-pi \
--class org.apache.spark.examples.SparkPi \
--conf spark.executor.instances=5 \
--conf spark.kubernetes.container.image=172.12.78.69:5000/spark:v1.7 \
local:///opt/spark/examples/jars/spark-examples_2.11-2.3.0.jar

spark-submit --master k8s://https://172.12.78.51:6443 \
--deploy-mode cluster \
--name spark-call-py \
--class py_wrapper.PythonWrapper \
--conf spark.executor.instances=5 \
--conf spark.kubernetes.container.image=172.12.78.69:5000/spark:v1.6 \
local:///opt/spark/examples/jars/PythonWrapper.jar \
/usr/bin/python3 /opt/spark/examples/py/test_spark_k8s.py 666

./spark-submit --master k8s://https://172.12.78.31:6443 \
--deploy-mode cluster \
--name spark-call-py \
--class py_wrapper.PythonWrapper \
--conf spark.executor.instances=5 \
--conf spark.kubernetes.container.image=172.12.78.69:5000/spark:v1.7 \
local:///opt/spark/examples/jars/PythonWrapper.jar \
/usr/bin/python3 /opt/spark/examples/py/pi.py 1000000 3

```
