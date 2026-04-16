import pytest
from app.transformation.worker import (
    create_heart_rate_observation,
    create_spo2_observation,
    create_blood_pressure_observation
)

@pytest.fixture
def sample_raw_data():
    return {
        "patient_id": "123456",
        "timestamp": "2026-04-16T12:00:00Z",
        "heart_rate": 85.0,
        "spo2": 98.0,
        "blood_pressure_systolic": 120.0,
        "blood_pressure_diastolic": 80.0,
        "device_id": "Device-ABC"
    }

def test_create_heart_rate_observation(sample_raw_data):
    obs = create_heart_rate_observation(sample_raw_data)
    assert obs is not None
    assert obs.status == "final"
    assert obs.code.coding[0].code == "8867-4"
    assert obs.subject.reference == "Patient/123456"
    assert obs.valueQuantity.value == 85.0
    assert obs.valueQuantity.unit == "beats/minute"

def test_create_spo2_observation(sample_raw_data):
    obs = create_spo2_observation(sample_raw_data)
    assert obs is not None
    assert obs.code.coding[0].code == "59408-5"
    assert obs.valueQuantity.value == 98.0
    assert obs.valueQuantity.unit == "%"

def test_create_blood_pressure_observation(sample_raw_data):
    obs = create_blood_pressure_observation(sample_raw_data)
    assert obs is not None
    assert obs.code.coding[0].code == "85354-9"
    assert len(obs.component) == 2
    
    systolic_comp = next((c for c in obs.component if c.code.coding[0].code == "8480-6"), None)
    diastolic_comp = next((c for c in obs.component if c.code.coding[0].code == "8462-4"), None)
    
    assert systolic_comp is not None
    assert systolic_comp.valueQuantity.value == 120.0
    
    assert diastolic_comp is not None
    assert diastolic_comp.valueQuantity.value == 80.0
