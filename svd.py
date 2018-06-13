#Author - Arush Kharbanda
#Date - 11 - June-2018


#Benchmarking Setup - Configure here for the benchmark size required
#sizes=[100,1000, 10000, 50000, 100000, 500000, 1000000]
sizes=[2]

#cores=[1,2,4,8,16,32,64,128]
cores=[1,2,4,8]

#Refer Assumption 1, change this if changing AWS instance type
cores_on_single_machine=4


import numpy as np
from pyspark import SparkContext, SparkConf
from pyspark.mllib.linalg.distributed import RowMatrix
from datetime import datetime
from pyspark.mllib.random import RandomRDDs
from pyspark.mllib.linalg import Vectors

benchmarks={}

#Function  to print the metrics
#TODO - Output text based matrix - check if needed
def print_metrics(benchmarks):
    for key in benchmarks.keys():
        print "Running Time Report " + key + " - " + str(benchmarks.get(key))

def g(x):
    print str(x)

def i (x):
    for a in x[1]:
        print "here"+ str(a),
    print str(x[0])+""


def j (x):
    for a in x:
        print "here"+ str(a),
    print ""

def h(x, a):
    a[x[0]] = x[1]

def p(x):
    x[1]


def transposeRowMatrix(m):
    transposedRowsRDD = m.rows.zipWithIndex()\
        .map(lambda x: rowToTransposedTriplet(x[0], x[1]))\
        .flatMap(lambda x: x)\
        .groupByKey()\
        .sortByKey()\
        .map(lambda x: x[1])\
        .map(lambda x: buildRow(x))
    #transposedRowsRDD = m.rows.zipWithIndex().map(lambda x:  rowToTransposedTriplet(x._1, x._2)).flatmap(lambda x:x).groupByKey().sortByKey().map(lambda  x:x._2).map(lambda x: buildRow(x))
    #.rows.zipWithIndex.map{case (row, rowIndex) => rowToTransposedTriplet(row, rowIndex)}.flatMap(x => x).groupByKey.sortByKey().map(_._2).map(buildRow)

    return RowMatrix(transposedRowsRDD)


def rowToTransposedTriplet(row, rowIndex):
    output=[]
    indexedRow = np.ndenumerate(row.toArray())
    for a,b in indexedRow:
        output.append((a[0], (rowIndex, long(b))))
    return output
    #indexedRow = row.toArray.zipWithIndex
    #indexedRow.map {case(value, colIndex) = > (colIndex.toLong, (rowIndex, value))}


def buildRow(rowWithIndexes):
    resArr = []
    for x in rowWithIndexes:
        resArr.insert(x[0], x[1])
    return Vectors.dense(resArr)



#Generate a array and requset it for all core configuration
for size in sizes:


    for core in cores:

        # Calculating spark configuration for a distributed setup
        executor_cores= cores_on_single_machine if core%cores_on_single_machine==0 else core%cores_on_single_machine
        executors=core/cores_on_single_machine if core%cores_on_single_machine==0 else core

        #Initializing Spark
        conf = SparkConf().setAppName("SVDBenchmarking")\
            .set("spark.executor.cores",executor_cores)\
            .set("spark.executor.instances",executors)
        sc = SparkContext.getOrCreate(conf=conf)

        start = datetime.now()

        inputRdd=sc.textfile("hdfs://localhost:8020/data/input"+size)
        inputRdd.foreach(lambda x: g(x))


        mat=RowMatrix(inputRdd)

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

