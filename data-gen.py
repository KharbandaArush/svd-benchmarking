#Benchmarking Setup - Configure here for the benchmark size required
#sizes=[100,1000, 10000, 50000, 100000, 500000, 1000000]
sizes=[100,1000]

from pyspark import SparkContext, SparkConf
from pyspark.mllib.random import RandomRDDs

conf = SparkConf().setAppName("SVD-Datagen") \
    .set("spark.executor.cores", 4) \
    .set("spark.executor.instances", 2)





sc = SparkContext.getOrCreate(conf=conf)

#TODO - configure the S3 bucket here
s3_bucket=""


for size in sizes:

    # Step 1 - Generating Data
    input = RandomRDDs.normalRDD(sc,size)



    # The diagonal values of A = 1:  A[i,i] = 1
    for j in range(size):
        input_array[j][j]=1