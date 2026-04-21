import logging
import os
import sys
import time

import cv2
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "video-stream")
FRAME_INTERVAL = float(os.environ.get("FRAME_INTERVAL", "0.04"))  # ~25 fps


def video_emitter(video_path: str) -> None:
    """Read a video file frame-by-frame and publish each frame as JPEG to Kafka."""
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
    capture = cv2.VideoCapture(video_path)

    if not capture.isOpened():
        logger.error("Unable to open video: %s", video_path)
        sys.exit(1)

    logger.info("Streaming %s to Kafka topic '%s' ...", video_path, KAFKA_TOPIC)
    frame_count = 0

    try:
        while capture.isOpened():
            success, image = capture.read()
            if not success:
                break

            ok, buffer = cv2.imencode(".jpg", image)
            if not ok:
                logger.warning("Failed to encode frame %d, skipping", frame_count)
                continue

            future = producer.send(KAFKA_TOPIC, buffer.tobytes())
            future.add_errback(lambda exc: logger.error("Kafka send error: %s", exc))

            frame_count += 1
            time.sleep(FRAME_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        capture.release()
        producer.flush()
        producer.close()
        logger.info("Done — sent %d frames", frame_count)


if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else "video.mp4"
    video_emitter(source)