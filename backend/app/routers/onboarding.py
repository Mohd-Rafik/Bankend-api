from fastapi import APIRouter, HTTPException
from app.schema import OnboardingRecord
from app.service import (
    get_onboarding_records,
    add_onboarding_record,
    delete_onboarding_record,
    update_onboarding_record,
)

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


def success_response(data=None, message="Success"):
    return {
        "status": "success",
        "message": message,
        "data": data,
    }


def error_response(message="Error"):
    return {
        "status": "error",
        "message": message,
        "data": None,
    }


@router.get("/list")
def list_records():
    data = get_onboarding_records()
    return success_response(data=data)


@router.post("/submit")
def submit_record(record: OnboardingRecord):
    data = add_onboarding_record(record)
    return success_response(data=data, message="Record created successfully")


@router.delete("/{item_id}")
def delete_record(item_id: str):
    if not delete_onboarding_record(item_id):
        raise HTTPException(status_code=404, detail=error_response(message="Record not found"))
    return success_response(message="Record deleted successfully")


@router.put("/{item_id}")
def update_record(item_id: str, record: OnboardingRecord):
    data = update_onboarding_record(item_id, record)
    if not data:
        raise HTTPException(status_code=404, detail=error_response(message="Record not found"))
    return success_response(data=data, message="Record updated successfully")
