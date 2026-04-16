import json
import os
from confluent_kafka import Consumer, KafkaError
from fhir.resources.observation import Observation, ObservationComponent
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from datetime import datetime
import uuid
import sys

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
SOURCE_TOPIC = 'raw-sensor-data'
GROUP_ID = 'fhir-converter-group'

def flush_print(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()

def create_consumer():
    """Creates and returns a Confluent Kafka Consumer instance."""
    try:
        conf = {
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'group.id': GROUP_ID,
            'auto.offset.reset': 'earliest'
        }
        consumer = Consumer(conf)
        consumer.subscribe([SOURCE_TOPIC])
        print(f"Connected to Kafka at {KAFKA_BOOTSTRAP_SERVERS}, listening on {SOURCE_TOPIC}")
        return consumer
    except Exception as e:
        print(f"Failed to connect to Kafka: {e}")
        return None

def create_heart_rate_observation(data):
    """Creates an FHIR Observation resource for Heart Rate."""
    try:
        obs = Observation(
            id=str(uuid.uuid4()),
            status="final",
            category=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/observation-category",
                            code="vital-signs",
                            display="Vital Signs"
                        )
                    ]
                )
            ],
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://loinc.org",
                        code="8867-4",
                        display="Heart rate"
                    )
                ]
            ),
            subject=Reference(reference=f"Patient/{data['patient_id']}"),
            effectiveDateTime=data['timestamp'],
            valueQuantity=Quantity(
                value=data['heart_rate'],
                unit="beats/minute",
                system="http://unitsofmeasure.org",
                code="/min"
            ),
            device=Reference(display=data['device_id'])
        )
        return obs
    except Exception as e:
        print(f"Error creating Observation: {e}")
        return None

def create_spo2_observation(data):
    """Creates an FHIR Observation resource for SpO2."""
    try:
        obs = Observation(
            id=str(uuid.uuid4()),
            status="final",
            category=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/observation-category",
                            code="vital-signs",
                            display="Vital Signs"
                        )
                    ]
                )
            ],
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://loinc.org",
                        code="59408-5",
                        display="Oxygen saturation in Arterial blood"
                    )
                ]
            ),
            subject=Reference(reference=f"Patient/{data['patient_id']}"),
            effectiveDateTime=data['timestamp'],
            valueQuantity=Quantity(
                value=data['spo2'],
                unit="%",
                system="http://unitsofmeasure.org",
                code="%"
            ),
            device=Reference(display=data['device_id'])
        )
        return obs
    except Exception as e:
        print(f"Error creating SpO2 Observation: {e}")
        return None

def create_blood_pressure_observation(data):
    """Creates an FHIR Observation resource for Blood Pressure."""
    try:
        obs = Observation(
            id=str(uuid.uuid4()),
            status="final",
            category=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system="http://terminology.hl7.org/CodeSystem/observation-category",
                            code="vital-signs",
                            display="Vital Signs"
                        )
                    ]
                )
            ],
            code=CodeableConcept(
                coding=[
                    Coding(
                        system="http://loinc.org",
                        code="85354-9",
                        display="Blood pressure panel with all children optional"
                    )
                ]
            ),
            subject=Reference(reference=f"Patient/{data['patient_id']}"),
            effectiveDateTime=data['timestamp'],
            device=Reference(display=data['device_id']),
            component=[
                ObservationComponent(
                    code=CodeableConcept(
                        coding=[Coding(system="http://loinc.org", code="8480-6", display="Systolic blood pressure")]
                    ),
                    valueQuantity=Quantity(
                        value=data['blood_pressure_systolic'],
                        unit="mmHg",
                        system="http://unitsofmeasure.org",
                        code="mm[Hg]"
                    )
                ),
                ObservationComponent(
                    code=CodeableConcept(
                        coding=[Coding(system="http://loinc.org", code="8462-4", display="Diastolic blood pressure")]
                    ),
                    valueQuantity=Quantity(
                        value=data['blood_pressure_diastolic'],
                        unit="mmHg",
                        system="http://unitsofmeasure.org",
                        code="mm[Hg]"
                    )
                )
            ]
        )
        return obs
    except Exception as e:
        print(f"Error creating BP Observation: {e}")
        return None

def run_worker():
    """Runs the transformation worker."""
    consumer = create_consumer()
    if not consumer:
        return

    print("Starting Transformation Worker...")
    
    try:
        while True:
            msg = consumer.poll(1.0) # Timeout 1.0s

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    flush_print(msg.error())
                    break

            raw_data = json.loads(msg.value().decode('utf-8'))
            flush_print(f"Received: {raw_data}")
            
            # Transform to FHIR
            observations_to_save = []
            
            hr_obs = create_heart_rate_observation(raw_data)
            if hr_obs: observations_to_save.append(("8867-4", hr_obs))
            
            spo2_obs = create_spo2_observation(raw_data)
            if spo2_obs: observations_to_save.append(("59408-5", spo2_obs))
            
            bp_obs = create_blood_pressure_observation(raw_data)
            if bp_obs: observations_to_save.append(("85354-9", bp_obs))
            
            for code, fhir_obs in observations_to_save:
                flush_print(f"Generated FHIR Resource: {fhir_obs.json()}")
                
                # Save to Database
                try:
                    from app.shared.database import SessionLocal, FHIRObservation
                    db = SessionLocal()
                    
                    db_obs = FHIRObservation(
                        resource_id=fhir_obs.id, 
                        patient_id=raw_data['patient_id'],
                        code=code, 
                        effective_datetime=raw_data['timestamp'],
                        resource_json=json.loads(fhir_obs.json())
                    )
                    db.add(db_obs)
                    db.commit()
                    flush_print(f"Saved Observation {code} for Patient {raw_data['patient_id']}")
                except Exception as db_err:
                    flush_print(f"Database Error: {db_err}")
                finally:
                    db.close()
            
    except KeyboardInterrupt:
        print("Worker stopped.")
    finally:
        consumer.close()

if __name__ == "__main__":
    run_worker()
