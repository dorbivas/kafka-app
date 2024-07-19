
import requests
import json
import time
from kafka import KafkaProducer

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers='my-kafka.default.svc.cluster.local:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Function to fetch data from API
def fetch_data():
    #url = "https://portal.thatapicompany.com/get?animal_type=dog"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to produce messages to Kafka
def produce():
    while True:
        data = fetch_data()
        if data:
            producer.send('test', data)
            print(f"Produced: {data}")
        else:
            print("Failed to fetch data")
        time.sleep(60)

if __name__ == "__main__":
    produce()

