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

    //val sizes =  Array (2)
    val sizes=Array (100,1000, 10000, 50000, 100000, 500000, 1000000)

    val conf = new  SparkConf().setAppName("SVD-Datagen").set("spark.executor.cores", "4").set("spark.executor.instances", "32" )

    val sc = new SparkContext(conf)
    for(size <- sizes)
      {
        val matrixA = MTUtils.randomDenVecMatrix(sc, size, size)
        matrixA.rows.foreach(println)
        val matrixB = matrixA.transpose()
        matrixB.blocks.foreach(println)
        val matrixC=matrixA.add(matrixB).divide(2)
        matrixC.getRows.foreach(println)
        val rddIntermid=matrixC.getRows.map(functiony)
        rddIntermid.foreach(println)



      }
    sc.stop()

  }
}
