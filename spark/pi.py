from __future__ import print_function

import sys
from random import random
from operator import add

from pyspark.sql import SparkSession
from pyspark import SparkConf


if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    sc_conf = SparkConf().setMaster("spark://172.12.78.32:30077")
    spark = SparkSession\
        .builder\
        .appName("PythonPi")\
        .config(conf=sc_conf)\
        .getOrCreate()

    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = 100000 * partitions

    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    print("Pi is roughly %f" % (4.0 * count / n))

    spark.stop()
