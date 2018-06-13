package edu.nju.pasalab.marlin.examples



import breeze.linalg.DenseVector

import edu.nju.pasalab.marlin.utils.MTUtils
import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.apache.spark.sql.Row


object SymmetricRandomMatrix {

  def functiony(x:Tuple2[Long,DenseVector[Double]]):Tuple2[Long,DenseVector[Double]]={
    x._2.data.update(x._1.toInt,1)
    x
  }
  def main(args: Array[String]) {

    val sizes =  Array (2)
    //val sizes=Array (100,1000, 10000, 50000, 100000, 500000, 1000000)

    val conf = new  SparkConf().setAppName("SVD-Datagen").set("spark.executor.cores", "4").set("spark.executor.instances", "32" ).setMaster("local[2]")
      .set("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version","2")
      .set("spark.speculation","false")
    val sc = new SparkContext(conf)
    sc.hadoopConfiguration.set("fs.s3.awsAccessKeyId", System.getenv("AWS_ACCESS_KEY"))
    sc.hadoopConfiguration.set("fs.s3.awsSecretAccessKey", System.getenv("AWS_SECRET_ACCESS_KEY"))
    sc.hadoopConfiguration.set("fs.s3.impl", "org.apache.hadoop.fs.s3.S3FileSystem")

    for(size <- sizes)
      {
        val matrixA = MTUtils.randomDenVecMatrix(sc, size, size)

        val matrixB = matrixA.transpose()

        val matrixC=matrixA.add(matrixB).divide(2)

        val rddIntermid=matrixC.getRows.map(functiony)
        rddIntermid.saveAsTextFile("hdfs://ip-172-31-12-0.us-west-1.compute.internal:8020/data/input"+size)
      }
    sc.stop()

  }
}
