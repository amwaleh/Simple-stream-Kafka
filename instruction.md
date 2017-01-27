![](https://cdn.scotch.io/15775/PRPg1998TfO6VKXTeaTz_illustration.jpg)
### What is kafka
Kafka is an opensource distributed streaming platform  that simplifies data intergration between systems.
A stream is a pipeline to which your applications can push data. You can find more info on kafka's [Official site](https://kafka.apache.org/documentation.html#gettingStarted)

Kafka system has three main component:
1. A Producer:  The service which produces the data that needs to be broadcast
2. A Broker:  This is Kafka itself , which acts as a middle man between the producer and the consumer. It utilises the power of API's to get and broadcast data
3. A Consumer: The service that utilises the data which the broker will broadcast.

### Installing Kafka

- If you are running mac OSX simply type `brew install kafka`
    - once done installing run `homebrew services start kafka`

- for linux user follow installation instruction from [here](https://www.tutorialspoint.com/apache_kafka/apache_kafka_installation_steps.htm)
- By default Kafka runs on port `91092`


### Project requirements:
 - Basic knowledge of python
 - python 3
 - Kafka [installed]((https://www.tutorialspoint.com/apache_kafka/apache_kafka_installation_steps.htm))
 - [Virtualenv](https://virtualenv.pypa.io/en/stable/).
 - pip installed


#### setting up :
 Create project directory  :
*  ` $ mkdir kafka  &&  cd kafka`

Create a virtualenv and activate it inside your project directory:
* `$ virtualenv env && source env/bin/activate`

Install required dependencies :
* `pip install kafka-python`

Our project will consist of:
- A simple producer that sends some data to kafka via the terminal
- A consumer that will fetch that sent data and display it.
- A kafka as the broker


### Creating  a Producer

A producer is a service that sends a message to the kafka broker.
The messaging instance needs a topic and the Mesaage.

**Lets creat it**

First require the `Kafkaclient`, this will help us connect to the kafka-broker by passing in the kafka url.

Next import the simpleProducer method from kafka, What this does is, it  connections to kafka broker through 'localhost:9092' (default address for kafka) and presents us with the `send_messages` function that will emit / send our message.

Next we need to declare our `Topic`.

Kafka uses topics to establish connection between consumers requests and the messages. Furthermore it uses this topics to organise and diffrentiate the various messages that are being broadcast.

A Consumer  must have the same topic as the message it needs to consume.

**Creating the message Message:**

The message will be passed as an argument from the Terminal, therefore we need to import `sys` and use the `argv` method.

**Sending  the message:**

Next we need to send the message once it has been entered.This achieved by calling the simpleProducer instance `producer` and call the `send_messages()` function. `send_messages` takes `a topic` and `message` argument.
Nb: the message has to in byte format hence we `encode` the message

Here is the full producer code

```python

  # producer.py
   from kafka import SimpleProducer, KafkaClient
   from sys import argv

   # Connect to kafka-broker
   kafka = KafkaClient('localhost:9092')

    # couple our broker to our producer
    producer = SimpleProducer(kafka)

    # add topic
    topic = 'my-topic'

    # Capture the message typed on the terminal
    msg = argv[1]
   # emit message to the broker
   producer.send_messages(topic, msg.encode())

```

Great !! we done with the producer

## Creating the Consumer

The consumer is a service that listens to what the kafker broker broadcasts. Each consumer service listens for a specific topic that is given to it.

To create a consumer we use the `KafkaConsumer` class from kafka.

- Next we pass the `topic` and the `bootstrap_servers` argument to it .
- The consumer `topic` has to be the same as the one contained in the .
Therefore pass `my-topic` to as the topic.
- Next lets pass our kafka server url as the `bootstrap_servers`

**Continuous Listening:**

We are now connected to our server and can listen to the topics being broadcasted.
Moreover, we need to continously get updates of new messages from the producer. To achieve this we introduce a loop. The loop will keep the connection open and update us once a message is received.

Here is the consumer.py code

```python
#consumer.py
from kafka import KafkaConsumer

#connect to Kafka server and pass the topic we want to consume
consumer = KafkaConsumer('lex-topic', bootstrap_servers=['0.0.0.0:9092'])

#Continuously listen to the connection and print messages as recieved
for msg in consumer:
	print(msg.value)
  ```

#### Running the program

You will need two terminal to run our application

- In the first terminal run  `consumer.py`.
  open a terminal and type:

  `(env)$ python consumer.py`

  ![](https://cdn.scotch.io/15775/cgXW3QWNSV2JdTLm9GWR_Screen%20Shot%202017-01-26%20at%203.46.53%20PM.png)

- In the second terminal run `producer.py` and pass in a message `"hello word"`

  `(env)$ python producer.py "hello world"`

  ![](https://cdn.scotch.io/15775/6vUxr6IISLm4Oe4KC1P8_Screen%20Shot%202017-01-26%20at%203.54.18%20PM.png)

Observe what happens on the terminal running consumer.py terminal
The message passed in the producer.py should appear in it
![](https://cdn.scotch.io/15775/SMvcFwwT36aVmWSktpoF_Screen%20Shot%202017-01-26%20at%203.54.32%20PM.png)


