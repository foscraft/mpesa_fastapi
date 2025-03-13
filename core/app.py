from fastapi import FastAPI, HTTPException
from models import PaymentRequest
from utils import get_access_token, generate_password
from config import SHORTCODE, CALLBACK_URL, STK_PUSH_URL
import requests

app = FastAPI(title="M-Pesa FastAPI Integration")

@app.post("/initiate-payment/")
async def initiate_payment(payment: PaymentRequest):
    """Initiate an STK Push payment request."""
    try:
        # Get access token
        access_token = get_access_token()
        
        # Generate password and timestamp
        password, timestamp = generate_password()
        
        # Prepare STK Push payload
        payload = {
            "BusinessShortCode": SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": str(payment.amount),
            "PartyA": payment.phone_number,  # Customer phone number
            "PartyB": SHORTCODE,             # Business shortcode
            "PhoneNumber": payment.phone_number,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": payment.account_reference,
            "TransactionDesc": f"Payment for {payment.account_reference}"
        }
        
        # Send STK Push request
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(STK_PUSH_URL, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to initiate STK Push")
        
        return response.json()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/callback/")
async def payment_callback(callback_data: dict):
    """Handle M-Pesa callback response."""
    # Log or process the callback data
    print("Callback received:", callback_data)
    
    # Check if payment was successful
    result_code = callback_data.get("Body", {}).get("stkCallback", {}).get("ResultCode")
    if result_code == 0:
        # Payment successful
        checkout_request_id = callback_data["Body"]["stkCallback"]["CheckoutRequestID"]
        amount = callback_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        return {"status": "success", "message": f"Payment of {amount} received", "checkout_request_id": checkout_request_id}
    else:
        # Payment failed
        result_desc = callback_data["Body"]["stkCallback"]["ResultDesc"]
        return {"status": "failed", "message": result_desc}