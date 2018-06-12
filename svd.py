#Author - Arush Kharbanda
#Date - 11 - June-2018


#Benchmarking Setup - Configure here for the benchmark size required
sizes=[100,1000, 10000, 50000, 100000, 500000, 1000000]
#sizes=[100,1000]

cores=[1,2,4,8,16,32,64,128]
#cores=[1,2,4,8]

#Refer Assumption 1, change this if changing AWS instance type
cores_on_single_machine=4


import numpy as np
from pyspark import SparkContext, SparkConf
from pyspark.mllib.linalg.distributed import RowMatrix
from datetime import datetime
from pyspark.mllib.random import RandomRDDs

benchmarks={}

#Function  to print the metrics
#TODO - Output text based matrix - check if needed
def print_metrics(benchmarks):
    for key in benchmarks.keys():
        print "Running Time Report " + key + " - " + str(benchmarks.get(key))

def g(x):
    print x


def transposeRowMatrix(m):
    m.rows.foreach(g)
    transposedRowsRDD = m.rows.zipWithIndex().foreach(g)
    #.rows.zipWithIndex.map{case (row, rowIndex) => rowToTransposedTriplet(row, rowIndex)}.flatMap(x => x).groupByKey.sortByKey().map(_._2).map(buildRow)
    RowMatrix(m)
    #RowMatrix(transposedRowsRDD)

'''
def rowToTransposedTriplet(row, rowIndex):
    indexedRow = row.toArray.zipWithIndex
    indexedRow.map{case (value, colIndex) => (colIndex.toLong, (rowIndex, value))}


def buildRow(rowWithIndexes):
    resArr = new Array[Double](rowWithIndexes.size)
    rowWithIndexes.foreach{case (index, value) =>resArr(index.toInt) = value}
    Vectors.dense(resArr)
'''


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

        # Step 1 - Generating Data
        randomRdd = RandomRDDs.normalRDD(sc, size)
        m=RowMatrix(randomRdd)
        transposeRowMatrix(m)


'''
        # The diagonal values of A = 1:  A[i,i] = 1
        for j in range(size):
            input_array[j][j] = 1

        #Starting clock for benchmark
        start=datetime.now()
        rows=sc.parallelize(input_array)


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
'''
print_metrics(benchmarks)

