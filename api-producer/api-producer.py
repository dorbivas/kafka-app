import os
import time
import requests
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

producer_config = {
    'bootstrap.servers': 'kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9092',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'sasl.username': 'user1',
    'sasl.password': 'I6ZUCTKN8y'
}

producer = Producer(producer_config)

cat_api_key = os.getenv('CAT_API_KEY')
dog_api_key = os.getenv('DOG_API_KEY')

msg_counter = 0

def create_topic():
    admin_client = AdminClient(producer_config)
    topic_list = ["breeds_topic"]
    existing_topics = admin_client.list_topics().topics

    if "breeds_topic" not in existing_topics:
        topic_list = [NewTopic("breeds_topic", num_partitions=3, replication_factor=1)]
        fs = admin_client.create_topics(topic_list)

        for topic, f in fs.items():
            try:
                f.result()
                print(f"Topic {topic} created successfully")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")
    else:
        print("Topic 'breeds_topic' already exists")


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
        print('Produced data messages: {}'.format(len(data)))
        print('Total messages sent so far: {}'.format(msg_counter))
        for item in data:
            if msg_counter >= 10:
                print('brokeloop')
                break
            producer.produce('breeds_topic', key=item['id'], value=str(item), callback=delivery_report)
            producer.poll(0)
        producer.flush()
        #print('Produced cat messages: {}'.format(len(cat_data)))
        #print('Produced dog messages: {}'.format(len(dog_data)))

        if msg_counter >= 10:
            msg_counter = 0    
        time.sleep(10)


if __name__ == "__main__":
    print("cheacking topic")
    create_topic()
    time.sleep(10)
    produce_data()






