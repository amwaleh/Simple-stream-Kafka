## producer.py

from kafka import SimpleProducer, KafkaClient
from sys import argv

# Connect to kafka-broker : provide the port at which kafka is running
kafka = KafkaClient('0.0.0.0:9092')

# couple our broker to our producer
producer = SimpleProducer(kafka)

# add topic
topic = 'my-topic'

# Capture the message typed on the terminal
msg = argv[1]

# Emit the message to kafka broker
producer.send_messages(topic, msg.encode())
