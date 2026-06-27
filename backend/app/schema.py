from typing import Optional
from pydantic import BaseModel, EmailStr


class Personal(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    date_of_birth: str
    gender: str


class Company(BaseModel):
    company_name: str
    company_email: EmailStr
    company_phone: str
    address: str
    industry: str
    website: Optional[str] = None


class OnboardingRecord(BaseModel):
    personal: Personal
    company: Optional[Company] = None
