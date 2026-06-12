import json
import time
import requests
from confluent_kafka import Producer

producer = Producer({
    "bootstrap.servers": "localhost:9092"
})

TOPIC = "public-transport-events"

def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed:", err)
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}]")

def fetch_transport_data():
    url = "https://api.tfl.gov.uk/line/bakerloo/arrivals"
    requests.get(url, timeout=10)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

while True:
    data = fetch_transport_data()

    event = {
        "source": "tfl-api",
        "fetched_at": time.time(),
        "payload": data
    }

    producer.produce(
        TOPIC,
        key="ovapi",
        value=json.dumps(event),
        callback=delivery_report
    )

    producer.flush()

    print("Sent transport API data to Kafka")

    time.sleep(30)