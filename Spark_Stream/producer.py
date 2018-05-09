import csv
import time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092',api_version=(0,10))
csvfile = open('test.csv','r')
reader = csv.reader(csvfile)

for line in reader:
    num = line[0]
    print(num)
    time.sleep(2)
    producer.send('number',num.encode('utf8'))