# M-Pesa Payment Integration with FastAPI

This project demonstrates how to integrate M-Pesa's Daraja API (STK Push - Lipa na M-Pesa Online) with a [FastAPI](https://fastapi.tiangolo.com/) application in Python. The implementation allows users to initiate payments via an STK Push prompt on their mobile phones and handles callbacks from M-Pesa to confirm transaction status.

## Features
- Generate M-Pesa OAuth access token for authentication.
- Initiate STK Push payment requests.
- Handle M-Pesa callback responses to verify payment success or failure.
- Built with FastAPI for fast, modern API development.

## Prerequisites
Before running the application, ensure you have the following:

1. **M-Pesa Daraja API Credentials**:
   - Register on the [Safaricom Developer Portal](https://developer.safaricom.co.ke/).
   - Create an app to obtain:
     - `Consumer Key`
     - `Consumer Secret`
     - `Shortcode` (Business Shortcode)
     - `Passkey` (Provided by Safaricom for live apps or sandbox testing).
2. **Python Environment**:
   - Python 3.8+
   - Install required packages:

```bash
pip install fastapi uvicorn requests pydantic
```
3. **Expose Local Server** (for testing):
   - Install [ngrok](https://ngrok.com/) to expose your local server for callback URLs:
```bash
ngrok http 8000
```

## Installation
1. Clone this repository:

```bash
git clone https://github.com/foscraft/mpesa_fastapi.git
cd pesa_fastapi
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. **Create a requirements.txt file with:**

```
fastapi
uvicorn
requests
pydantic
```


## Usage

1. **Run the FastAPI Server:**
```bash
uvicorn core.app:app --reload
```

   - The server will start at http://127.0.0.1:8000.

2. **Expose the Server with ngrok:**

    - Start ngrok to get a public URL:

```bash
ngrok http 8000
```

   - Update the CALLBACK_URL in main.py with the ngrok URL (e.g., https://your-ngrok-url.ngrok.io/callback).

3. **Initiate a Payment:**
    - Send a POST request to /initiate-payment/ with the following JSON payload:

```json

{
  "phone_number": "254712345678",
  "amount": 100.0,
  "account_reference": "Order123"
}
```

**Example using curl:**

```bash

curl -X POST "http://127.0.0.1:8000/initiate-payment/" \
     -H "Content-Type: application/json" \
     -d '{"phone_number": "254712345678", "amount": 100.0, "account_reference": "Order123"}'
```

- Check your phone for the STK Push prompt and enter your M-Pesa PIN.

4. **Monitor Callback:**
    - M-Pesa will send a response to the /callback/ endpoint after the transaction.
    - The response is logged to the console (e.g., success or failure details).
    - Example success response:
```json

{
  "status": "success",
  "message": "Payment of 100 received",
  "checkout_request_id": "ws_CO_13032025123456789"
}
```

## Configuration
- **Sandbox vs. Live:**
    - The current setup uses sandbox URLs (https://sandbox.safaricom.co.ke/...).
    - For production, replace with live URLs (https://api.safaricom.co.ke/...) and use live credentials.

- **Security:**
    - Store sensitive credentials (e.g., CONSUMER_KEY, PASSKEY) in environment variables using a .env file and python-dotenv for better security.

## Example `.env` File

```plaintext

CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
SHORTCODE=your_shortcode
PASSKEY=your_passkey
CALLBACK_URL=https://your-ngrok-url/callback
```

Update main.py to load these variables:

```python

from dotenv import load_dotenv
import os

load_dotenv()
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
SHORTCODE = os.getenv("SHORTCODE")
PASSKEY = os.getenv("PASSKEY")
CALLBACK_URL = os.getenv("CALLBACK_URL")
```

## Notes
- `Error Handling:` Basic error handling is included. Enhance it for production use.
- `Database:` For a real application, store transaction details in a database (e.g., PostgreSQL) instead of printing to the console.
- `Testing:` Use the Safaricom sandbox environment for testing with test phone numbers (e.g., 254708374149).

## Troubleshooting
- `STK Push Not Appearing:` Ensure the phone number is in the correct format (2547XXXXXXXX) and the sandbox/live environment matches your credentials.
- `Callback Not Received:` Verify the CALLBACK_URL is publicly accessible and matches the URL registered with Safaricom.
