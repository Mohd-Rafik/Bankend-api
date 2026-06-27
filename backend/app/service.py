import json
import os
import uuid
from datetime import datetime

from app.schema import OnboardingRecord

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PERSONAL_FILE = os.path.join(BASE_DIR, "personal.json")
COMPANY_FILE = os.path.join(BASE_DIR, "company.json")


def read_json(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def get_personal_records():
    return read_json(PERSONAL_FILE)


def get_company_records():
    return read_json(COMPANY_FILE)


def get_onboarding_records():
    personal_records = get_personal_records()
    company_records = get_company_records()
    company_map = {item["id"]: item for item in company_records}

    combined = []
    for personal in personal_records:
        combined.append({
            **personal,
            "company": company_map.get(personal["id"]),
        })

    combined.sort(key=lambda record: record.get("created_at", ""), reverse=True)
    return combined


def add_onboarding_record(record: OnboardingRecord):
    payload = record.model_dump()
    created_at = datetime.now().isoformat()
    item_id = uuid.uuid4().hex

    personal_record = {
        **payload["personal"],
        "id": item_id,
        "created_at": created_at,
    }

    personal_data = get_personal_records()
    personal_data.append(personal_record)
    write_json(PERSONAL_FILE, personal_data)

    company_record = None
    company_payload = payload.get("company")
    if company_payload and any(value not in (None, "") for value in company_payload.values()):
        company_record = {
            **company_payload,
            "id": item_id,
            "created_at": created_at,
        }
        company_data = get_company_records()
        company_data.append(company_record)
        write_json(COMPANY_FILE, company_data)

    return {
        **personal_record,
        "company": company_record,
    }


def delete_onboarding_record(item_id):
    personal_data = get_personal_records()
    company_data = get_company_records()

    new_personal = [item for item in personal_data if item["id"] != item_id]
    new_company = [item for item in company_data if item["id"] != item_id]

    if len(personal_data) == len(new_personal):
        return False

    write_json(PERSONAL_FILE, new_personal)
    write_json(COMPANY_FILE, new_company)
    return True


def update_onboarding_record(item_id, record: OnboardingRecord):
    payload = record.model_dump()
    personal_data = get_personal_records()
    company_data = get_company_records()
    now = datetime.now().isoformat()

    updated_personal = None
    for index, item in enumerate(personal_data):
        if item["id"] == item_id:
            personal_data[index] = {
                **payload["personal"],
                "id": item_id,
                "created_at": item.get("created_at", now),
            }
            updated_personal = personal_data[index]
            break

    if updated_personal is None:
        return None

    write_json(PERSONAL_FILE, personal_data)

    company_payload = payload.get("company")
    if company_payload and any(value not in (None, "") for value in company_payload.values()):
        found = False
        for index, item in enumerate(company_data):
            if item["id"] == item_id:
                company_data[index] = {
                    **company_payload,
                    "id": item_id,
                    "created_at": item.get("created_at", now),
                }
                found = True
                break

        if not found:
            company_data.append({
                **company_payload,
                "id": item_id,
                "created_at": now,
            })

        write_json(COMPANY_FILE, company_data)
    else:
        company_data = [item for item in company_data if item["id"] != item_id]
        write_json(COMPANY_FILE, company_data)

    company_record = next((item for item in company_data if item["id"] == item_id), None)
    return {
        **updated_personal,
        "company": company_record,
    }
