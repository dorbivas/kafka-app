import time
from kafka import KafkaProducer
import json

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers='my-kafka.default.svc.cluster.local:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def produce():
    while True:
        message = {"message": "test"}
        producer.send('test', message)
        print(f"Produced: {message}")
        time.sleep(60)  # Sends a message every 60 seconds

if __name__ == "__main__":
    produce()
