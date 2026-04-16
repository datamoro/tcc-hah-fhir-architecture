from fastapi import APIRouter, Depends, HTTPException
from app.api import auth
from sqlalchemy.orm import Session
from app.shared.database import get_engine, SessionLocal, FHIRObservation
from typing import List, Optional

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/Observation")
def search_observations(
    patient: Optional[str] = None,
    code: Optional[str] = None,
    db: Session = Depends(get_db),
    token_payload: dict = Depends(auth.verify_token)
):
    query = db.query(FHIRObservation)
    
    if patient:
        # Check if patient param includes "Patient/" prefix
        patient_id = patient.split('/')[-1] if '/' in patient else patient
        query = query.filter(FHIRObservation.patient_id == patient_id)
    
    if code:
        query = query.filter(FHIRObservation.code == code)
        
    results = query.limit(100).all()
    
    # Return list of FHIR resources (JSON)
    return [res.resource_json for res in results]
