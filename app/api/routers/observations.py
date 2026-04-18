from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.api import auth
from app.shared.database import AsyncSessionLocal, FHIRObservation

router = APIRouter()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/Observation")
async def search_observations(
    patient: Optional[str] = None,
    code:    Optional[str] = None,
    db:      AsyncSession  = Depends(get_db),
    _:       dict          = Depends(auth.verify_token),
):
    stmt = select(FHIRObservation)

    if patient:
        patient_id = patient.split('/')[-1] if '/' in patient else patient
        stmt = stmt.where(FHIRObservation.patient_id == patient_id)

    if code:
        stmt = stmt.where(FHIRObservation.code == code)

    stmt = stmt.order_by(FHIRObservation.effective_datetime.desc()).limit(100)

    result = await db.execute(stmt)
    rows = result.scalars().all()

    # Return ORJSONResponse directly: bypasses jsonable_encoder and Pydantic
    # validation entirely. Safe because resource_json is already a JSON-compatible
    # Python dict validated by fhir.resources at write time.
    return ORJSONResponse(content=[row.resource_json for row in rows])
