from fastapi import FastAPI
from app.api.routers import observations
from app.api import auth
from app.shared.database import init_db

app = FastAPI(
    title="Hospital-at-Home FHIR API",
    description="API for accessing physiological data in FHIR format.",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"status": "online", "service": "Hospital-at-Home API"}

app.include_router(auth.router, prefix="/auth", tags=["Security / SMART on FHIR"])
app.include_router(observations.router, prefix="/fhir", tags=["Observations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)
