import time
import requests
from confluent_kafka import Producer

# Kafka Producer Configuration
producer_config = {
    'bootstrap.servers': 'kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9092',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'sasl.username': 'user1',
    'sasl.password': '2VxxUQUFJP'
}

producer = Producer(producer_config)

# Hardcoded API Keys
cat_api_key = 'live_jRspfxAS9kUNq55CSurmJLScxtFFT9QongDE3IffWbPaziujpkzzOmgLT44ToEco'
dog_api_key = 'live_kM1boQGZ4B0zy5DfLQX4axOZeMriiKr51Z6g806UPh5LftbVv7vvuSveBZI2pgau'


def fetch_cat_data():
    headers = {'x-api-key': cat_api_key}
    response = requests.get('https://api.thecatapi.com/v1/images/search?limit=10', headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def fetch_dog_data():
    headers = {'x-api-key': dog_api_key}
    response = requests.get('https://api.thedogapi.com/v1/images/search?limit=10', headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def produce_data():
    while True:
        cat_data = fetch_cat_data()
        dog_data = fetch_dog_data()
        data = cat_data + dog_data
        for item in data:
            producer.produce('breeds_topic', key=item['id'], value=str(item), callback=delivery_report)
            producer.poll(0)
        producer.flush()
        time.sleep(60)

if __name__ == "__main__":
    produce_data()
