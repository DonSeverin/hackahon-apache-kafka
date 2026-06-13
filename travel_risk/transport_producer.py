import json
import os
import time
from confluent_kafka import Producer

from travel_risk.risk.core import (
    calculate_risk,
    risk_level,
    build_commute_risk_event,
    )



producer = Producer({
    "bootstrap.servers": "localhost:9092"
})

def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed:", err)
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}]")


while True:
    event = build_commute_risk_event()

    producer.produce(
        TOPIC,
        key="commute-risk",
        value=json.dumps(event),
        callback=delivery_report
    )

    producer.flush()

    print(f"Sent commute risk score: {event['risk_level'].upper()} {event['risk_score']}/100")

    time.sleep(POLL_SECONDS)
