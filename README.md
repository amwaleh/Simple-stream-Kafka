# Simple Kafka Video Stream

![Kafka Video Streaming](https://cdn.scotch.io/15775/PRPg1998TfO6VKXTeaTz_illustration.jpg)

A minimal example of **real-time video streaming with Apache Kafka** — a producer reads a video file frame-by-frame and publishes JPEG frames to a Kafka topic, while a Flask consumer serves them as an MJPEG stream in the browser.

## What is Kafka?

Kafka is an open-source distributed streaming platform that simplifies data integration between systems.
See the [official docs](https://kafka.apache.org/documentation.html#gettingStarted) for more info.

**Three main components:**

1. **Producer** — the service that publishes data
2. **Broker** — Kafka itself, the middleware that stores and delivers messages
3. **Consumer** — the service that reads and processes the data

## Architecture

### High-Level Flow

```mermaid
flowchart LR
    A["🎬 Video File\n(video.mp4)"] -->|"OpenCV\nread frames"| B["📤 Producer\n(producer.py)"]
    B -->|"JPEG bytes"| C["📦 Kafka Broker\n(localhost:9092)"]
    C -->|"topic: video-stream"| D["📥 Consumer\n(consumer.py)"]
    D -->|"MJPEG stream"| E["🌐 Browser\n(localhost:5000)"]
```

### Detailed Data Flow

```mermaid
sequenceDiagram
    participant V as 🎬 Video File
    participant P as 📤 Producer
    participant K as 📦 Kafka Broker
    participant C as 📥 Consumer<br/>(Background Thread)
    participant F as 🖥️ Flask Server
    participant B as 🌐 Browser

    P->>V: Open video capture
    loop Every frame (~25 fps)
        V->>P: Read frame (BGR image)
        P->>P: Encode frame as JPEG
        P->>K: Send JPEG bytes to topic
    end
    P->>K: Flush & close

    Note over C,K: Runs continuously in background
    loop Consume messages
        K->>C: Deliver message
        C->>C: Store latest frame in shared buffer
    end

    B->>F: GET /
    loop Stream response
        F->>F: Read latest frame from buffer
        F->>B: Yield MJPEG frame
    end
```

### Component Architecture

```mermaid
graph TB
    subgraph Producer ["producer.py"]
        P1[OpenCV VideoCapture] --> P2[JPEG Encoder]
        P2 --> P3[KafkaProducer]
    end

    subgraph Broker ["Kafka Broker"]
        T[Topic: video-stream<br/>Partition 0]
    end

    subgraph Consumer ["consumer.py"]
        C1[KafkaConsumer<br/>Background Thread]
        C2[Shared Frame Buffer<br/>Thread-safe]
        C3[Flask HTTP Server]
        C1 --> C2
        C2 --> C3
    end

    P3 -->|publish| T
    T -->|subscribe| C1
    C3 -->|"multipart/x-mixed-replace"| B1[Browser Client 1]
    C3 -->|"multipart/x-mixed-replace"| B2[Browser Client 2]
    C3 -->|"multipart/x-mixed-replace"| B3[Browser Client N]
```

## Prerequisites

- Python 3.10+
- Apache Kafka running on `localhost:9092` (default)

### Installing Kafka

- **macOS:** `brew install kafka && brew services start kafka`
- **Linux:** follow the [official quickstart](https://kafka.apache.org/quickstart)
- **Docker:** `docker run -d --name kafka -p 9092:9092 apache/kafka`

## Setup

```bash
git clone https://github.com/amwaleh/Simple-stream-Kafka.git
cd Simple-stream-Kafka
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

You need **two terminals**:

**Terminal 1 — Producer** (reads `video.mp4` and sends frames to Kafka):

```bash
python producer.py              # default: video.mp4
python producer.py myvideo.avi  # or specify a file
```

**Terminal 2 — Consumer** (Flask server that streams frames to the browser):

```bash
python consumer.py
```

Open your browser at **http://localhost:5000**

## Configuration

All settings can be overridden with environment variables:

| Variable | Default | Description |
|---|---|---|
| `KAFKA_BROKER` | `localhost:9092` | Kafka bootstrap server |
| `KAFKA_TOPIC` | `video-stream` | Kafka topic name |
| `FRAME_INTERVAL` | `0.04` | Seconds between frames (~25 fps) |
| `PORT` | `5000` | Flask server port |
