![](https://cdn.scotch.io/15775/PRPg1998TfO6VKXTeaTz_illustration.jpg)
### What is kafka
Kafka is an opensource distributed streaming platform  that simplifies data integration between systems.
A stream is a pipeline to which your applications receives data continously.
As a streaming platform kafka has two primary uses:
* Data Integration: Kafka captures streams of events or data changes and feeds these to other data systems such as relational databases, key-value stores or  data warehouses.
* Stream processing: Kafka accepts each stream of event and stores it in an append only queue  called a log.Information in the log is immutable hence enables continuous, real-time processing and transformation of these streams and makes the results available system-wide.

Compared to other technologies, Kafka has a better throughput, built-in partitioning, replication, and fault-tolerance which makes it a good solution for large scale message processing applications.

Kafka system has three main components:
1. A Producer:  The service which produces the data that needs to be broadcast
2. A Broker:  This is Kafka itself , which acts as a middle man between the producer and the consumer. It utilises the power of API's to get and broadcast data
3. A Consumer: The service that utilises the data which the broker will broadcast.

You can find more info on kafka's [Official site](https://kafka.apache.org/documentation.html#gettingStarted)
## Project
We are going to build a simple streaming  application, that  streams a video file from our producer and display it in a web browser. The main purpose of this project is to showcase  Data integration and stream processing properties of kafka.

## Project requirements:
*NB: This project aims to introduce the basics of Kafka and Messaging. It assumes you have basic knowledge on Python.*

 - Basic knowledge of python
 - python 3
 - Kafka [installed]((https://www.tutorialspoint.com/apache_kafka/apache_kafka_installation_steps.htm))
 - [Virtualenv](https://virtualenv.pypa.io/en/stable/).
 - [pip](https://pip.pypa.io/en/stable/installing/) installed

## Installing Kafka

- If you are running mac OSX simply type `brew install kafka`
    - once done installing run `brew services start kafka`

- for linux user follow installation instruction from [here](https://www.tutorialspoint.com/apache_kafka/apache_kafka_installation_steps.htm)
- By default Kafka runs on port `9092`

This project aims to introduce you to the basics of Kafka and Messaging,  and assumes you have basic knowledge on Python.


## Setting up :
Our project will consist of:
- A video file that will be our source of data
- A simple producer that sends video images to Kafka
- A consumer that will fetch the sent data and display it on a web browser.
- and finally Kafka as the broker

Create project directory  :
*  ` $ mkdir kafka  &&  cd kafka`

Create a virtualenv and activate it inside your project directory:
* `$ virtualenv env && source env/bin/activate`

Install required dependencies :
We need to install [Flask](http://flask.pocoo.org/) and [opencv](http://opencv-python-tutroals.readthedocs.io/)
* `pip install kafka-python opencv-python Flask`


## Creating  the Producer

A producer is a service that sends messages to the kafka broker.
One thing to note is , the producer is not concerned with the various systems that will eventually consume or load the broadcast data.

**Lets create it**

First require the `Kafkaclient` from `kafka`, this will help us connect to the kafka-broker by passing in the kafka url.

Next import the simpleProducer method from kafka, What this does is, it  connects to kafka broker through the address `localhost:9092` (default address for kafka) and presents us with the `send_messages` function that will emit / send our message.

Next we need to declare our `Topic`.

Kafka uses topics to establish connection between consumers requests and the messages. Furthermore it uses this topics to organise and differentiate the various messages that are being broadcast.

A Consumer  must have the same topic as the message it needs to consume.

**Creating the Message:**

The message will consist of images sent in binary form. To achieve this we use **Opencv ** library. Opencv enables us to read our movie file and convert it into bytes, before sending it to Kafka.
We need to create a function that will take in a video file, read the file and converting the file  into bytes before sending it  to kafka.  For this tutorial, I advise placing the video file in the same folder as the producer.

**Sending  the message:**

Once the file  has been read it needs to be sent to Kafka.This is achieved by calling the `producer` instance and invoking the `send_messages()` function. `send_messages` takes `a topic` and `message` argument.
Nb: the message has to in byte format hence we encode the image using `jpeg.tobytes()`

Here is the full producer code

```python
# producer.py
import time
import cv2
from kafka import SimpleProducer, KafkaClient
#  connect to Kafka
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)
# Assign a topic
topic = 'my-topic'


def video_emitter(video):
    # Open the video
    video = cv2.VideoCapture(video)
    print(' emitting.....')

    # read the file
    while (video.isOpened):
        # read the image in each frame
        success, image = video.read()

        # check if the file has read the end
        if not success:
            break

        # convert the image png
        ret, jpeg = cv2.imencode('.png', image)
        # Convert the image to bytes and send to kafka
        producer.send_messages(topic, jpeg.tobytes())
        # To reduce CPU usage create sleep time of 0.2sec
        time.sleep(0.2)
    # clear the capture
    video.release()
    print('done emitting')


if __name__ == '__main__':
    video_emitter('video.mp4')
```

Great !! we done with the producer

## Creating the Consumer

The consumer is a service that listens and consumes what the kafka broker broadcasts. Each consumer service listens for a specific topic  given to it.

Our consumer will listen to the all messages with a topic `my-topic`  from Kafka and  display them. We shall be using [Flask](http://flask.pocoo.org/) - A python microframework  to display the recieved video images.

To create a consumer we use the `KafkaConsumer` class from kafka.
- Next we pass the `topic` and the `bootstrap_servers` argument to it .
- The consumer `topic` has to be the same as the one contained in the message.
Therefore pass `my-topic`  as the topic.
- Next  pass  `localhost:9092` url  as the `bootstrap_servers`
- Finally we pass a `group_id` for fetching an committing offsets ( offsets is a marker that helps the broker to identify the last message it read by the consumer)

**Continuous Listening:**

We need to continuously get updates of new messages from the broker. To achieve this we introduce a generator function. A generator is a function that produces a sequence of results instead of a single value.It will keep the connection open and update us once a message is received . This will enables us to recieve a continous stream of images immidately they are sent. Lets call our function `kafka_stream`.

Note, the images will be sent in part and for the purpose of having a stream where each part replaces the previous part the `multipart/x-mixed-replace content` type must be used when displaying the images.

Here is the consumer.py code

```python
from flask import Flask, Response
from kafka import KafkaConsumer

#connect to Kafka server and pass the topic we want to consume
consumer = KafkaConsumer('my-topic', group_id='view' bootstrap_servers=['0.0.0.0:9092'])


#Continuously listen to the connection and print messages as recieved
app = Flask(__name__)


@app.route('/')
def index():
    # return a multipart response
    return Response(kafkastream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
def kafkastream():

    for msg in consumer:
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + msg.value + b'\r\n\r\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

```


## Running the program
First and foremost make sure Kafka is working by running `brew services kafka`.

next open two terminal

- In the first terminal run  `producer`.
  open a terminal and type:

  `(env)$ python producer.py`
  ![](https://cdn.scotch.io/15775/T1cgynmnTj2Vtz0Ih8Dv_producer.jpg)

- In the second terminal run `consumer.py`

  `(env)$ python consumer.py`
  ![](https://cdn.scotch.io/15775/tZD4cMBqTamBmzoE3sXE_consumer.jpg)

This will run our flask web server.

Next open your browser and navigate to `http://0.0.0.0:5000` ,
![](https://cdn.scotch.io/15775/Bn9desdVTraaEn9azvDb_Screen%20Shot%202017-02-04%20at%207.38.50%20PM.png)

## Observations
1. When the browser is refreshed the video does not restart .Kafka uses message offset to know how far in the log the consumer had read.
2. If you close the browser while the video is playing the next time you reopen the browser the video picks from where you left it.
3. The producer does not need to be running for  the video to play. Kafka stores the message and avails when the consumer is ready to recieve the message.
4. When both  Producer and Consumer are running the video is recieved almost in real time.
5. The video are processed in a sequential FIFO manner.
6. One message can be shared amongst many Consumers. This reduces the number of request thats would have been made to the producer if it were an API.


## Where to use Kafka:

- Microservices : If  you are developing your software application using Micro-Services, Kafka has proved to be the best conduit for the various services that need to continously communicate asynchronously with each other.

- Databases:  Data warehouse constantly need to backup or replication data. One way of not of dumping whole databases is to create kafka producers and consumers that detect and  save only changes (diff) made to the databases . Moreover producers can be used together with ORM signals  to trigger the replication process.

- Log  Data:  Producers can be embeded on websites to collect  click events or page views in realtime.
- security cameras
- Sensor and  device data
- stock ticker

## Conclusion :

 Kafka is an awesome messaging system that is fast, scalable and easy to use.  You only need to  know which topic to publish and which topic you to consume in order to use the system.
we created a simple python streaming project demonstrates the advantages of streaming data,How fast it can be and how Kafka works as a broker.

