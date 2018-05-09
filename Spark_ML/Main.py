# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 16:45:50 2017

@author: swang
"""
# Set up environment
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.mllib.util import MLUtils
from pyspark.ml.regression import LinearRegression

def ReadTrainSet(sc):
	# Init SparkSQL
	sql_sc = SQLContext(sc)

	# Read Data Frame in LibSVM format
	train = spark.read.format('libsvm').load('Train_Dataset_Cleaned_Sample.txt')
	
	print('--- Finished importing training dataset')
	print(' The training set has ' + str(train.count()) + ' lines of records')
	
	return train

def ApplyLR(sc,train):	
	print('--- Start train the Linear Regression Model')
	lr = LinearRegression(maxIter = 10, regParam = 0.3, elasticNetParam = 0.8)
	lrModel = lr.fit(train)

	print("Coefficients: %s" % str(lrModel.coefficients))
	print("Intercept: %s" % str(lrModel.intercept))

	# Summarize the model over the training set and print out some metrics
	trainingSummary = lrModel.summary
	print("numIterations: %d" % trainingSummary.totalIterations)
	print("objectiveHistory: %s" % str(trainingSummary.objectiveHistory))
	trainingSummary.residuals.show()
	print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
	print("r2: %f" % trainingSummary.r2)

if __name__ == '__main__':
	conf = (SparkConf()
		 .setMaster("local[1]") 
		 .setAppName("Shi App"))
	sc = SparkContext(conf = conf)
	spark = SparkSession(sc)
	train = ReadTrainSet(sc)
	ApplyLR(sc,train)
	sc.stop()
