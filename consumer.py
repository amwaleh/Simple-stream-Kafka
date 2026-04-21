import logging
import os
import threading

from flask import Flask, Response
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "video-stream")

app = Flask(__name__)

# Shared latest-frame buffer so multiple clients can view the stream
# without competing for the same Kafka consumer.
_latest_frame = None
_frame_lock = threading.Lock()


def _kafka_reader():
    """Background thread: consume Kafka messages and keep the latest frame."""
    global _latest_frame
    logger.info("Kafka reader started — broker=%s topic=%s", KAFKA_BROKER, KAFKA_TOPIC)
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset="latest",
    )
    try:
        for msg in consumer:
            with _frame_lock:
                _latest_frame = msg.value
    finally:
        consumer.close()


def _generate_stream():
    """Yield MJPEG frames from the shared buffer."""
    while True:
        with _frame_lock:
            frame = _latest_frame
        if frame is not None:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
            )


@app.route("/")
def index():
    return Response(
        _generate_stream(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


# Start the background Kafka reader once on import
_reader_thread = threading.Thread(target=_kafka_reader, daemon=True)
_reader_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
