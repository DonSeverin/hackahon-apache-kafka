import json
import time

from confluent_kafka import Producer

from travel_risk.config import KAFKA_BOOTSTRAP_SERVERS, POLL_SECONDS, TOPIC
from travel_risk.risk.core import (
    build_commute_risk_event,
    delivery_report,
)


producer = Producer({
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS
})


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
