import os
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

sc=SparkContext(appName = 'Test_Stream')
sc.setLogLevel('WARN')

ssc = StreamingContext(sc,2)

KafkaStream = KafkaUtils.createDirectStream(ssc, ['number'], \
                                            {'metadata.broker.list': 'localhost:9092'})

parsed = KafkaStream.map(lambda num: num[1])
parsed.pprint()

ssc.start()
ssc.awaitTermination()