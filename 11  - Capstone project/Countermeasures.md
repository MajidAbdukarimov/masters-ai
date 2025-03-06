# Security Best Practices for Database Query Assistant

This README outlines the security measures implemented in the Database Query Assistant project to protect sensitive data, prevent common vulnerabilities, and ensure secure operation. Following these best practices is essential for maintaining the security and integrity of the application.

## 1. API Key Exposure Protection

### Security Issue
Hardcoding sensitive information like API keys, database credentials, and other secrets directly in the code can lead to exposure in public repositories or logs.

### Countermeasure
- Use environment variables to store sensitive data
- Use a `.env` file with the dotenv package to load secrets securely

```python
# Example with dotenv for loading API keys
from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from a .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
```

**Important:** Make sure your `.env` file is in `.gitignore` so it's not committed to version control:
```
.env
```

## 2. SQL Injection Prevention

### Security Issue
If your application executes SQL queries based on user input directly, malicious users might be able to manipulate SQL queries to perform unauthorized actions, like accessing or modifying data.

### Countermeasure
- Always use parameterized queries to prevent SQL injection
- Avoid concatenating user inputs directly in SQL queries

```python
import sqlite3

def safe_query(query, params):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute(query, params)  # Safe query with parameters
    result = cursor.fetchall()
    conn.close()
    return result

# Example usage
query = "SELECT * FROM products WHERE product_code = ?"
params = (user_input_product_code,)
result = safe_query(query, params)
```

## 3. Secure Data Transmission

### Security Issue
If sensitive data is transmitted over the network (e.g., API keys, user information), it's vulnerable to being intercepted by attackers if not encrypted.

### Countermeasure
- Use HTTPS for all communication between the client and server to ensure data is encrypted in transit
- Ensure your API service enforces HTTPS connections

```python
# Example of using HTTPS for API requests
import requests

response = requests.get("https://api.openai.com/v1/engines", headers={"Authorization": f"Bearer {OPENAI_API_KEY}"})
```

## 4. Authentication and Authorization

### Security Issue
Weak or missing authentication and authorization mechanisms can allow unauthorized users to access certain parts of the system.

### Countermeasure
- Implement strong authentication (e.g., OAuth, JWT, API keys)
- Ensure role-based authorization is used, where users have access only to the resources they are permitted to

```python
import jwt
from datetime import datetime, timedelta

# Generating JWT token
def generate_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Example of verifying JWT token
def verify_jwt(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
```

## 5. Secure Logging Practices

### Security Issue
If your logging contains sensitive data (e.g., user input, passwords, or API keys), attackers could access sensitive information.

### Countermeasure
- Ensure sensitive data is not logged
- Mask or remove sensitive information from logs

```python
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

def log_sensitive_action(user_input):
    # Never log sensitive data directly
    sanitized_input = "REDACTED"
    logging.info(f"User requested an action with input: {sanitized_input}")
```

## 6. Cross-Site Scripting (XSS) Protection

### Security Issue
If user input is displayed on the front-end without proper sanitization, it may allow attackers to inject malicious scripts into the UI, affecting other users.

### Countermeasure
- Sanitize user input before displaying it on the UI (e.g., escape HTML)
- Use libraries or frameworks that automatically handle XSS protection

```python
import streamlit as st
import html

user_input = st.text_input("Enter your query")
sanitized_input = html.escape(user_input)
st.write(f"Your input: {sanitized_input}")
```

## 7. Rate Limiting Implementation

### Security Issue
An attacker could potentially overload your system with requests, either via brute force attacks or a DDoS (Distributed Denial of Service) attack.

### Countermeasure
- Implement rate limiting to restrict the number of requests a user can make in a certain time frame

```python
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

@app.route("/some-api")
@limiter.limit("5 per minute")  # Allow 5 requests per minute per IP
def some_api():
    return "API Response"
```

## 8. Session Management

### Security Issue
Weak session management, such as not expiring sessions or not invalidating them after a logout, can lead to unauthorized access if a session token is hijacked.

### Countermeasure
- Implement session expiration (e.g., expire sessions after a certain period of inactivity)
- Invalidate sessions upon logout or password change

```python
from flask import session
import time
from datetime import timedelta

# Set session expiration time (in seconds)
session.permanent = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Invalidate session after logout
session.pop('user_id', None)
```

## Implementation Checklist

- [ ] Add `.env` file and load environment variables for sensitive data
- [ ] Refactor database queries to use parameterized queries and avoid SQL injection
- [ ] Use HTTPS for API calls
- [ ] Implement authentication mechanisms like JWT for security
- [ ] Sanitize user input and use proper logging practices
- [ ] Add rate limiting to protect against DoS attacks
- [ ] Ensure proper session management to prevent session hijacking

Following these security best practices will help ensure that your Database Query Assistant remains secure against common vulnerabilities and threats.
