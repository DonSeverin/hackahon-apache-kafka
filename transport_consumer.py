import json
from confluent_kafka import Consumer, Message

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "transport-consumer-group",
    "auto.offset.reset": "earliest"
})

consumer.subscribe(["public-transport-events"])

print("Listening for transport events...")

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

    print("\nReceived event:")
    print("Source:", event.get("source"))
    print("Fetched at:", event.get("fetched_at"))

    payload = event.get("payload")

    if isinstance(payload, dict):
        print("Payload type: dict")
        print("Payload keys:", list(payload.keys()))

    elif isinstance(payload, list):
        print("Payload type: list")
        print("Number of items:", len(payload))

        if len(payload) > 0:
            print("First item:")
            print(json.dumps(payload[0], indent=2)[:1000])

    else:
        print("Payload type:", type(payload))
        print("Payload:", payload)