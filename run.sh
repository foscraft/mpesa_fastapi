curl -X POST "http://127.0.0.1:8000/initiate-payment/" \
    -H "Content-Type: application/json" \
    -d '{"phone_number": "254712345678", "amount": 100.0, "account_reference": "Order123"}'