from typing import Optional
from pydantic import BaseModel


class Personal(BaseModel):
    full_name: str
    email: str
    phone: str
    date_of_birth: str
    gender: str


class Company(BaseModel):
    company_name: str
    company_email: str
    company_phone: str
    address: str
    industry: str
    website: Optional[str] = ""


class OnboardingRecord(BaseModel):
    personal: Personal
    company: Company