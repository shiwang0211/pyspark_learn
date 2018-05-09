from kafka import KafkaConsumer

consumer = KafkaConsumer('number',api_version=(0,10))
for num in consumer:
    print(num.value.decode('utf8'))
