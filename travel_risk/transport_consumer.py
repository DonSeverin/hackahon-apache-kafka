import json
from confluent_kafka import Consumer, Message
from travel_risk.config import KAFKA_BOOTSTRAP_SERVERS, TOPIC


consumer = Consumer({
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "group.id": "transport-consumer-group",
    "auto.offset.reset": "earliest"
})

consumer.subscribe([TOPIC])

print("Listening for commute risk events...")

while True:
    msg: Message | None = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print("Consumer error:", msg.error())
        continue

    msg_value: bytes | None = msg.value()
    if msg_value is None:
        print("Received message with null value")
        continue
    
    event = json.loads(msg_value.decode("utf-8"))

    if event.get("event_type") != "commute_risk_score":
        print("\nReceived unknown event:")
        print(json.dumps(event, indent=2)[:1000])
        continue

    print(f"\n{event.get('from')} -> {event.get('to')}")
    print(f"Risk: {event.get('risk_level', 'unknown').upper()} {event.get('risk_score')}/100")
    print("Lines:", ", ".join(event.get("lines_checked", [])))

    print("Reasons:")
    for reason in event.get("reasons", []):
        print(f"- {reason}")
