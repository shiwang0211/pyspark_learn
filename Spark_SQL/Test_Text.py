import pyspark
sc = pyspark.SparkContext()
rdd = sc.parallelize(['Hello,', 'worlddddd!'])
words = sorted(rdd.collect())
print words
temp = sc.textFile("gs://dataproc-08b834aa-82f4-42c5-b794-67fc46a96d4d-us" + "test_SXW.py")
print '88888' + temp.count + '88888'
