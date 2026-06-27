from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schema import OnboardingRecord
from app.service import (
    get_onboarding_records,
    add_onboarding_record,
    delete_onboarding_record,
    update_onboarding_record,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "API Running"}


@app.get("/onboarding/list")
def onboarding_list():
    return get_onboarding_records()


@app.post("/onboarding/submit")
def onboarding_submit(record: OnboardingRecord):
    return add_onboarding_record(record)


@app.delete("/onboarding/{id}")
def delete(id: str):

    if not delete_onboarding_record(id):
        raise HTTPException(404, "Record not found")

    return {"message": "Deleted Successfully"}


@app.put("/onboarding/{id}")
def update(id: str, record: OnboardingRecord):

    data = update_onboarding_record(id, record)

    if not data:
        raise HTTPException(404, "Record not found")

    return data
