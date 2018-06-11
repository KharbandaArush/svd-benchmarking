#Script for genrating data
#sizes=[100,1000, 10000, 50000, 100000, 500000, 1000000]
sizes=[100,1000]
#cores=[1,2,4,8,16,32]
cores=[1,2,4,8]
import numpy as np
import array
sizes=array.array('i',[4,5])
from pyspark import SparkContext, SparkConf
from pyspark.mllib.linalg.distributed import RowMatrix
from datetime import datetime
benchmarks={}

for size in sizes:

    # Step 1 - Generating Data
    b = np.random.rand(size, size)
    input_array = (b + b.T) / 2

    # The diagonal values of A = 1:  A[i,i] = 1
    for j in range(size):
        input_array[j][j]=1

    #check random array
    print('\n'.join(['    '.join(['{:10}'.format(item) for item in row])
                     for row in input_array]))

    #Step-2
    #running SVD
    for core in cores:
        executor_cores= 4 if core%4==0 else core%4
        executors=core/4 if core%4==0 else core
        conf = SparkConf().setAppName("SVDBenchmarking")\
            .set("spark.executor.cores",executor_cores)\
            .set("spark.executor.instances",executors)

        sc = SparkContext.getOrCreate(conf=conf)

        start=datetime.now()
        rows=sc.parallelize(input_array)

        mat = RowMatrix(rows)
        svd = mat.computeSVD(size, computeU=True)
        U = svd.U  # The U factor is a RowMatrix.
        s = svd.s  # The singular values are stored in a local dense vector.
        V = svd.V  # The V factor is a local dense matrix.

        end = datetime.now()

        running_time=end-start

        benchmarks[str(size)+'_'+str(core)]=running_time

        sc.stop()

for key in benchmarks.keys():
    print key + " - " +benchmarks.get(key)