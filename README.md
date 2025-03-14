M-Pesa Payment Integration with FastAPI
======================================
This project provides a robust integration of M-Pesa's Daraja API (STK Push - Lipa na M-Pesa Online) with a FastAPI application in Python. It enables users to initiate payments via an STK Push prompt on their mobile phones and processes callbacks from M-Pesa to confirm transaction status.

## Features
- Generate M-Pesa OAuth access token for secure API authentication.
- Initiate STK Push payment requests to prompt users for payment on their mobile devices.
- Handle M-Pesa callback responses to verify payment success or failure.
- Input validation using Pydantic for secure and reliable request handling.
- Comprehensive error handling for timeouts, network issues, and API errors.
- Logging for debugging and monitoring transaction flow.
- Built with FastAPI for high-performance, modern API development.

## Prerequisites
Before running the application, ensure you have the following:

### M-Pesa Daraja API Credentials:
- Register on the Safaricom Developer Portal.
- Create an app to obtain:
  - Consumer Key
  - Consumer Secret
  - Shortcode (Business Shortcode)
  - Passkey (Provided by Safaricom for live apps; use the sandbox passkey for testing).
- For sandbox testing, use test credentials provided by Safaricom (e.g., phone number: 254708374149).

### Python Environment:
- Python 3.8 or higher.
- Install required packages after setting up the project (see Installation).

### Expose Local Server (for Testing):
- Install Ngrok to expose your local server for callback URLs, as M-Pesa requires a publicly accessible HTTPS URL:
  - Download and install Ngrok.
  - Run `ngrok http 8000` to get a public URL (e.g., `https://your-ngrok-url.ngrok.io`).

## Installation
Follow these steps to set up the project:

### Clone the Repository:
```sh
git clone https://github.com/foscraft/mpesa_fastapi.git
cd mpesa_fastapi
```

### Set Up a Virtual Environment (optional but recommended):
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies:
Ensure you have a `requirements.txt` file with the following content:
```sh
fastapi==0.115.0
uvicorn==0.30.6
requests==2.32.3
python-dotenv==1.0.1
pydantic==2.9.2
```
Then install the dependencies:
```sh
pip install -r requirements.txt
```

### Configure Environment Variables:
Create a `.env` file in the project root with your M-Pesa credentials:
```ini
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
SHORTCODE=174379
PASSKEY=bfb279f9aa9bdbcf158e87dd71a887cd2e0c893059b10f78e6b72ada1ed2c808
CALLBACK_URL=https://your-ngrok-url.ngrok.io/callback/
```
Replace the values with your actual credentials. For sandbox testing, use the provided sandbox passkey.

## Usage
### Run the FastAPI Server:
```sh
python main.py
```
The server will start at `http://127.0.0.1:8000`.

Use `--reload` for development to enable auto-reload on code changes:
```sh
uvicorn main:app --reload
```

### Expose the Server with Ngrok:
Start Ngrok to get a public HTTPS URL:
```sh
ngrok http 8000
```
Update the `CALLBACK_URL` in your `.env` file with the Ngrok URL (e.g., `https://your-ngrok-url.ngrok.io/callback/`).

### Initiate a Payment:
Send a `POST` request to `/initiate-payment/` with the following JSON payload:
```json
{
  "phone_number": "254712345678",
  "amount": 100.0,
  "account_reference": "Order123"
}
```

Example using `curl`:
```sh
curl -X POST "http://127.0.0.1:8000/initiate-payment/" \
     -H "Content-Type: application/json" \
     -d '{"phone_number": "254712345678", "amount": 100.0, "account_reference": "Order123"}'
```
Check your phone for the STK Push prompt and enter your M-Pesa PIN to complete the payment.

### Monitor Callback:
M-Pesa will send a response to the `/callback/` endpoint after the transaction is processed.

Example success response:
```json
{
  "status": "success",
  "message": "Payment of 100 received",
  "checkout_request_id": "ws_CO_13032025123456789"
}
```

Example failure response:
```json
{
  "status": "failed",
  "message": "The transaction was canceled by the user"
}
```

## Deployment to Production
### HTTPS Setup:
- M-Pesa requires the `CALLBACK_URL` to be an HTTPS endpoint.
- Deploy the application to a server with a valid SSL certificate (e.g., AWS, Heroku, or DigitalOcean).
- Use a reverse proxy like Nginx with Let’s Encrypt for SSL.

### Use a WSGI Server:
Run the application with a production-grade server like Gunicorn:
```sh
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Database Integration:
Store transaction details (e.g., `CheckoutRequestID`, amount, status) in a database like PostgreSQL for persistence and auditing.

### Security:
- Validate callback requests to ensure they originate from M-Pesa (e.g., check the source IP address).
- Rotate API credentials periodically and use a secrets management solution.

### Monitoring:
- Configure logging to write to a file or a logging service (e.g., ELK stack, CloudWatch) for monitoring and debugging.

## Troubleshooting
### STK Push Not Appearing:
- Ensure the phone number is in the correct format (`2547XXXXXXXX`).
- Verify that your credentials match the environment (sandbox or live).
- Check if the `CALLBACK_URL` is correctly set and publicly accessible.

### Callback Not Received:
- Confirm that the `CALLBACK_URL` is an HTTPS URL and matches the URL registered with Safaricom.
- Use Ngrok to expose your local server during testing.
- Check server logs for errors or network issues.

### Access Token Errors:
- Verify that `CONSUMER_KEY` and `CONSUMER_SECRET` are correct.
- Ensure the `AUTH_URL` matches your environment (sandbox or live).

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

