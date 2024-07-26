import os
import time
import requests
from confluent_kafka import Producer

producer_config = {
    'bootstrap.servers': 'kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9092',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'sasl.username': 'user1',
    'sasl.password': 'pJCjiaiua4'
}

producer = Producer(producer_config)
time.sleep(10)
# Hardcoded API Keys
cat_api_key = 'live_jRspfxAS9kUNq55CSurmJLScxtFFT9QongDE3IffWbPaziujpkzzOmgLT44ToEco'
dog_api_key = 'live_kM1boQGZ4B0zy5DfLQX4axOZeMriiKr51Z6g806UPh5LftbVv7vvuSveBZI2pgau'

# cat_api_key = os.getenv('CAT_API_KEY')
# dog_api_key = os.getenv('DOG_API_KEY')

# print("CAT_API_KEY:", os.getenv('CAT_API_KEY'))
# print("DOG_API_KEY:", os.getenv('DOG_API_KEY'))

msg_counter = 0



def fetch_cat_data():
    headers = {'x-api-key': cat_api_key}
    response = requests.get('https://api.thecatapi.com/v1/images/search?limit=5', headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def fetch_dog_data():
    headers = {'x-api-key': dog_api_key}
    response = requests.get('https://api.thedogapi.com/v1/images/search?limit=5', headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def delivery_report(err, msg):
    global msg_counter
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        msg_counter += 1
        print('Message delivered to {} partition: {}'.format(msg.topic(), msg.partition()))
        print('Total messages sent: {}'.format(msg_counter))

def produce_data():
    global msg_counter
    while True:
        cat_data = fetch_cat_data()
        dog_data = fetch_dog_data()
        data = cat_data + dog_data
        for item in data:
            if msg_counter >= 10:
                print('brokeloop')
                break
            producer.produce('breeds_topic', key=item['id'], value=str(item), callback=delivery_report)
            producer.poll(0)
        producer.flush()
        print('Produced cat messages: {}'.format(len(cat_data)))
        print('Produced dog messages: {}'.format(len(dog_data)))
        print('Produced data messages: {}'.format(len(data)))
        print('Total messages sent so far: {}'.format(msg_counter))
        if msg_counter >= 10:
            msg_counter = 0    
        time.sleep(60)


if __name__ == "__main__":
    produce_data()






