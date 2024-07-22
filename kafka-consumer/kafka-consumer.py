from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'test',
    bootstrap_servers='my-kafka.default.svc.cluster.local:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def consume():
    for message in consumer:
        print(f"Consumed: {message.value}")

if __name__ == "__main__":
    consume()