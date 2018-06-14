#Author - Arush Kharbanda
#Date - 11 - June-2018


#Benchmarking Setup - Configure here for the benchmark size required
sizes=[100,1000, 10000, 50000, 100000, 500000, 1000000]
cores=[1,2,4,8,16,32,64]



#Refer Assumption 1, change this if changing AWS instance type
max_cores_for_a_single_executor=8



from pyspark import SparkContext, SparkConf
from pyspark.mllib.linalg.distributed import RowMatrix
from datetime import datetime
from pyspark.mllib.random import RandomRDDs
from pyspark.mllib.linalg import Vectors

benchmarks={}

def textToVector(x):
    array=str(x).replace('(','').replace(')','').replace('DenseVector','').split(',')
    return (int(array[0]), Vectors.dense(array[1:]))


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
        executor_cores= max_cores_for_a_single_executor if core>max_cores_for_a_single_executor else core
        executors=1 if core/max_cores_for_a_single_executor==0 else core/max_cores_for_a_single_executor


        #Initializing Spark
        conf = SparkConf().setAppName("SVDBenchmarking")\
            .set("spark.executor.cores",executor_cores)\
            .set("spark.executor.instances",executors) \
            .set("spark.dynamicAllocation.enabled","false")\
            .set("spark.driver.maxResultSize","6g")\
            .set("spark.executor.memory", "60g")\
        # .set("spark.default.parallelism", str(21474836))\

        sc = SparkContext.getOrCreate(conf=conf)

        start = datetime.now()

        inputRdd=sc.textFile("hdfs://ip-172-31-34-253.us-west-2.compute.internal:8020/data/input"+str(size))
        #inputRdd=sc.textFile("/Users/arushkharbanda/data/input"+str(size))
        intermid2=inputRdd\
            .map(lambda x: textToVector(x))\
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

        benchmarks[str(size) +" x " +str(size) +' with '+str(core)+ " cores (Executors="+str(executors)+", Executor Cores="+str(executor_cores)+")"]=running_time

        #Freeing up spark cluster
        print_metrics(benchmarks)
        sc.stop()

print_metrics(benchmarks)

