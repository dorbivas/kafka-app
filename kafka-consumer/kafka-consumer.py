from confluent_kafka import Consumer, KafkaException, KafkaError
import os

# Kafka Consumer Configuration
consumer_config = {
    'bootstrap.servers': 'kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9092',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'sasl.username': os.getenv('KAFKA_USER'),
    'sasl.password': os.getenv('KAFKA_PASS'),
    'group.id': 'breeds_group',
    'auto.offset.reset': 'latest'
}

consumer = Consumer(consumer_config)
consumer.subscribe(['breeds_topic'])

msg_rec_count = 0

def consume_data():
    global msg_rec_count
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            msg_rec_count += 1
            print('{} : Received message: {}'.format(msg_rec_count, msg.value().decode('utf-8')))
    finally:
        consumer.close()

if __name__ == "__main__":

    consume_data()
