#Author - Arush Kharbanda
#Date - 11 - June-2018


#Benchmarking Setup - Configure here for the benchmark size required
sizes=[100,1000, 10000, 50000, 100000, 500000, 1000000]
cores=[1,2,4,8,16,32,64, 128]


#Refer Assumption 1, change this if changing AWS instance type
cores_on_single_machine=16


import numpy as np
from pyspark import SparkContext, SparkConf
from pyspark.mllib.linalg.distributed import RowMatrix
from datetime import datetime
from pyspark.mllib.random import RandomRDDs
from pyspark.mllib.linalg import Vectors

benchmarks={}

def textToVector(x):
    array=str(x).replace('(','').replace(')','').replace('DenseVector','').split(',')
    return (int(array[0]), Vectors.dense(array[1],array[2]))


def extract(x):
    return Vectors.dense(x[1])


#Function  to print the metrics
#TODO - Output text based matrix - check if needed
def print_metrics(benchmarks):
    for key in benchmarks.keys():
        print "Running Time Report " + key + " - " + str(benchmarks.get(key))

def g(x):
    print "output"+str(x)

#Generate a array and requset it for all core configuration
for size in sizes:


    for core in cores:

        # Calculating spark configuration for a distributed setup
        executor_cores= cores_on_single_machine if core%cores_on_single_machine==0 else core%cores_on_single_machine
        executors=core/cores_on_single_machine if core%cores_on_single_machine==0 else core

        #Initializing Spark
        conf = SparkConf().setAppName("SVDBenchmarking")\
            .set("spark.executor.cores",executor_cores)\
            .set("spark.executor.instances",executors)\
            .set("spark.default.parallelism", str(size))\
            .set("spark.executor.memory", "30g")

        sc = SparkContext.getOrCreate(conf=conf)

        start = datetime.now()

        inputRdd=sc.textFile("hdfs://ip-172-31-39-44.us-west-2.compute.internal:8020/input"+str(size))
        intermid2=inputRdd.map(lambda x: textToVector(x))\
            .sortByKey()\
            .map(lambda x: extract(x))

        mat=RowMatrix(intermid2)

        # Step-2
        # running SVD
        svd = mat.computeSVD(size, computeU=True)
        U = svd.U  # The U factor is a RowMatrix.
        s = svd.s  # The singular values are stored in a local dense vector.
        V = svd.V  # The V factor is a local dense matrix.

        # Stoping clock for benchmark
        end = datetime.now()

        running_time=end-start

        benchmarks[str(size) +" x " +str(size) +' with '+str(core)+ " cores"]=running_time

        #Freeing up spark cluster
        sc.stop()

print_metrics(benchmarks)

