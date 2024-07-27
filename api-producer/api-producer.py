import os
import time
import requests
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

producer_config = {
    'bootstrap.servers': 'kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9092',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'sasl.username': os.getenv('KAFKA_USER'),
    'sasl.password': os.getenv('KAFKA_PASS')
}
producer = Producer(producer_config)

cat_api_key = os.getenv('CAT_API_KEY')
dog_api_key = os.getenv('DOG_API_KEY')

TOPIC_NAME = "breeds_topic"
msg_counter = 0

def create_topic():
    #handle topic create when kafka empty
    admin_client = AdminClient(producer_config)
    topic_list = [TOPIC_NAME]
    existing_topics = admin_client.list_topics().topics

    if TOPIC_NAME not in existing_topics: 
        topic_list = [NewTopic(TOPIC_NAME, num_partitions=3, replication_factor=1)]
        topics = admin_client.create_topics(topic_list)

        for topic, item in topics.items():
            try:
                item.result()
                print(f"Topic {topic} created successfully")

            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")
    else:
        print("breeds_topic already exists")

def fetch_data(api_url, api_key):
    headers = {'x-api-key': api_key}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
        
    return None

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
        cat_data = fetch_data('https://api.thecatapi.com/v1/images/search?limit=5', cat_api_key)
        dog_data = fetch_data('https://api.thedogapi.com/v1/images/search?limit=5', dog_api_key)
        data = cat_data + dog_data

        for item in data:
            #limit production to 10 msgs 
            if msg_counter >= 10:
                break
            producer.produce(TOPIC_NAME, key=item['id'], value=str(item), callback=delivery_report)
            producer.poll(0)

        producer.flush()
        print('Produced data messages: {}'.format(len(data)))
        print('Total messages sent so far: {}'.format(msg_counter))
        if msg_counter >= 10:
            msg_counter = 0  

        time.sleep(60)


if __name__ == "__main__":
    print("cheacking topics...")
    create_topic()
    time.sleep(10)
    produce_data()






