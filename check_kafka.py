from confluent_kafka import Producer, Consumer
import json
import time

conf_p = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf_p)

topic = 'test-verification'

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

print("producing...")
producer.produce(topic, json.dumps({"foo": "bar"}).encode('utf-8'), callback=delivery_report)
producer.flush()

print("consuming...")
conf_c = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'test-group-1',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf_c)
consumer.subscribe([topic])

msg = consumer.poll(10.0)
if msg is None:
    print("No message received")
else:
    print(f"Received message: {msg.value().decode('utf-8')}")

consumer.close()
