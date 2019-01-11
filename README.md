![](https://cdn.scotch.io/15775/PRPg1998TfO6VKXTeaTz_illustration.jpg)
### What is kafka
Kafka is an opensource distributed streaming platform  that simplifies data intergration between systems.
A stream is a pipeline to which your applications can push data. You can find more info on kafka's [Official site](https://kafka.apache.org/documentation.html#gettingStarted)

Kafka system has three main component:

1. A Producer: The service which produces the data that needs to be broadcast

2. A Broker: This is Kafka itself, which acts as a middle man between the producer and the consumer. It utilises the power of API's to get and broadcast data

3. A Consumer: The service that utilises the data which the broker will broadcast

### Installing Kafka

- If you are running mac OSX simply type `brew install kafka`
    - once done installing run `brew services start kafka`

- for linux user follow installation instruction from [here](https://www.tutorialspoint.com/apache_kafka/apache_kafka_installation_steps.htm)
- By default Kafka runs on port `9092`


### Project requirements:
 - Basic knowledge of python
 - python 3
 - Kafka [installed]((https://www.tutorialspoint.com/apache_kafka/apache_kafka_installation_steps.htm))
 - [Virtualenv](https://virtualenv.pypa.io/en/stable/).
 - pip installed


#### setting up :
clone this repo:
* `$ git clone git@github.com:amwaleh/Simple-stream-Kafka.git`

Create a virtualenv and activate it inside your project directory:
* `$ virtualenv env && source env/bin/activate`

Install required dependencies
* `pip install kafka-python opencv-python Flask`


## Running the program

You will need two terminal to run the application

In the first terminal run consumer.py. open a terminal and type:

`(env)$ python producer.py`



In the second terminal run producer.py and pass in a message "hello word"

`(env)$ python consumer.py`



Open your browser and navigate to `http://0.0.0.0:5000`
