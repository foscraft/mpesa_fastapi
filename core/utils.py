import base64
import datetime
import requests
from fastapi import HTTPException
from config import CONSUMER_KEY, CONSUMER_SECRET, AUTH_URL, SHORTCODE, PASSKEY

def get_access_token() -> str:
    """Generate an OAuth access token from M-Pesa."""
    auth = base64.b64encode(f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    response = requests.get(AUTH_URL, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get access token")
    
    return response.json()["access_token"]

def generate_password() -> tuple[str, str]:
    """Generate the password and timestamp for STK Push."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{SHORTCODE}{PASSKEY}{timestamp}".encode()).decode()
    return password, timestamp