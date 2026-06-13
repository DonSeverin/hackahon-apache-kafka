# hackahon-apache-kafka

Learning how to implement Kafka into systems using live TfL transport data.

## Project Flow

This project has 3 main parts:

```text
TfL API -> Producer -> Kafka -> Consumer -> Terminal output
```

## What Each Part Does

### 1. Kafka

Kafka is the message box.

The producer sends messages into Kafka, and the consumer reads messages from Kafka.

Start Kafka first:

```bash
docker compose up -d
```

### 2. Producer

The producer is `transport_producer.py`.

It does this every 30 seconds:

```text
asks TfL for line status
calculates commute risk
sends the result to Kafka
```

Run it in a separate terminal:

```bash
python transport_producer.py
```

Example output:

```text
Delivered to commute-risk [0]
Sent commute risk score: LOW 0/100
```

### 3. Consumer

The consumer is `transport_consumer.py`.

It waits for messages from Kafka and prints them nicely.

Run it in a separate terminal:

```bash
python transport_consumer.py
```

Example output:

```text
Listening for commute risk events...

Stratford -> Paddington
Risk: LOW 0/100
Lines: central, jubilee, elizabeth
Reasons:
- Central has good service
- Jubilee has good service
- Elizabeth has good service
```

## Run Order

You need 3 terminals.

### Terminal 1: Start Kafka

```bash
docker compose up -d
```

### Terminal 2: Start Consumer

```bash
python transport_consumer.py
```

### Terminal 3: Start Producer

```bash
python transport_producer.py
```

