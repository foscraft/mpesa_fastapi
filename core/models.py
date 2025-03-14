from pydantic import BaseModel, Field, constr, validator
from typing import Optional

class PaymentRequest(BaseModel):
    phone_number: constr(min_length=12, max_length=12) = Field(
        ..., example="254712345678", description="Phone number in international format (e.g., 254712345678)"
    )
    amount: float = Field(..., ge=1.0, example=100.0, description="Amount to be paid in KES (minimum 1.0)")
    account_reference: constr(min_length=1, max_length=12) = Field(
        ..., example="Order123", description="Account reference for the transaction (max 12 characters)"
    )

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if not v.startswith("254") or not v.isdigit():
            raise ValueError("Phone number must start with '254' and contain only digits")
        return v

    @validator("amount")
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        if v > 150000:
            raise ValueError("Amount exceeds M-Pesa transaction limit of 150,000 KES")
        return v

# Models for callback validation (optional, but recommended)
class CallbackMetadataItem(BaseModel):
    Name: str
    Value: str

class StkCallback(BaseModel):
    ResultCode: int
    ResultDesc: str
    CheckoutRequestID: Optional[str] = None
    CallbackMetadata: Optional[dict] = None

class CallbackBody(BaseModel):
    stkCallback: StkCallback

class CallbackData(BaseModel):
    Body: CallbackBody