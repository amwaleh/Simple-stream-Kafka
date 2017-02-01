# consumer.py

from kafka import KafkaConsumer

# initialise our connection to Kafka server and pass the topic we want from it
consumer = KafkaConsumer('pulse-topic', group_id='my_group', bootstrap_servers=['0.0.0.0:9092'])

# Conitiously listen to the connection and print messages as recieved
for msg in consumer:
  print(msg.value)
