from pydantic import BaseModel

class PaymentRequest(BaseModel):
    phone_number: str  # e.g., "254712345678"
    amount: float      # e.g., 100.0
    account_reference: str  # e.g., "Order123"