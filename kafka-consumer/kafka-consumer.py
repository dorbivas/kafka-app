from confluent_kafka import Consumer, KafkaException, KafkaError
import os

# Kafka Consumer Config
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

consume_count = 0
def consume_data():
    global consume_count
    try:
        while True:
            msg = consumer.poll(1.0)
            #handle empty msg
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF: 
                    continue
                else:
                    print(msg.error())
                    break
            consume_count += 1
            #emit to stdout
            print('{} : Received message: {}'.format(consume_count, msg.value().decode('utf-8'))) 
    finally:
        consumer.close()

if __name__ == "__main__":

    consume_data()
