import json
import time
import random
import os
from confluent_kafka import Producer
from datetime import datetime, timezone

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
TOPIC_NAME = 'raw-sensor-data'

def create_producer():
    """Creates and returns a Confluent Kafka Producer instance."""
    try:
        producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})
        print(f"Connected to Kafka at {KAFKA_BOOTSTRAP_SERVERS}")
        return producer
    except Exception as e:
        print(f"Failed to connect to Kafka: {e}")
        return None

def generate_vital_signs(patient_id):
    """Generates synthetic vital signs data."""
    return {
        "patient_id": patient_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": f"wearable-{patient_id}",
        "heart_rate": random.randint(60, 100),
        "spo2": random.randint(95, 100),
        "blood_pressure_systolic": random.randint(110, 130),
        "blood_pressure_diastolic": random.randint(70, 85)
    }

def run_simulation():
    """Runs the sensor simulation."""
    producer = create_producer()
    if not producer:
        return

    print("Starting sensor simulation...")
    patient_ids = ["P001", "P002", "P003"]

    try:
        while True:
            for pid in patient_ids:
                data = generate_vital_signs(pid)
                producer.produce(TOPIC_NAME, json.dumps(data).encode('utf-8'))
                producer.poll(0)
                print(f"Sent: {data}")

            time.sleep(1)  # Simulate 1 second interval
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        producer.flush()
        print("Producer closed.")

if __name__ == "__main__":
    run_simulation()
