# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 16:45:50 2017

@author: swang
"""
# Set up environment
from pyspark import SparkConf, SparkContext
from pyspark import SQLContext
from pyspark.sql.functions import *
from pyspark.sql.types import *

def SummariseVolume(sc):

	# Init SparkSQL
	sql_sc = SQLContext(sc)

	# Read Data Frame from Google Cloud Storage
	df_1 = sql_sc.read.csv('gs://dataproc-08b834aa-82f4-42c5-b794-67fc46a96d4d-us/sps_data_sample_160218_300-400.csv',\
		header = True)
	df_2 = sql_sc.read.csv('gs://dataproc-08b834aa-82f4-42c5-b794-67fc46a96d4d-us/Signals.csv',\
		header = True)

	# Optional, import from hdfs
	# df_ = spark.read.csv('hdfs:///spm/dataset/sps_data_sample_160218_300-400.csv', header = True)

	time_pattern = 'yyyy/MM/dd HH:mm:ss'

	df =df_1.filter((df_1['EventCode'] == 82) & (df_1['SignalID'] < 1150)) \
		.withColumn('Time', unix_timestamp('Timestamp', time_pattern).cast('timestamp'))\
		.groupBy('SignalID',window('Time','5 minutes')) \
		.agg(count('EventCode').alias('Volume'))
	df.select(df.window.start.cast('string').alias('Timestart'),'*') \
		.orderBy(['SignalID']) \
		.join(df_2, df_1.SignalID == df_2.Signal_Id, 'inner') \
		.select('SignalID', 'Timestart','Volume','Primary_Name','Secondary_Name','Latitude','Longitude') \
		.write.format('csv').options(header = "true").save('gs://dataproc-08b834aa-82f4-42c5-b794-67fc46a96d4d-us/output.csv')

if __name__ == '__main__':
	conf = (SparkConf()#https://spark.apache.org/docs/latest/submitting-applications.html#master-urls
		 .setMaster("yarn") 
		 .setAppName("Shi App"))
	sc = SparkContext(conf = conf)
	SummariseVolume(sc)






