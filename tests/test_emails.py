import pytest
from fastapi.testclient import TestClient
from main import app
from models import EmailAnalysis, Intent
from unittest.mock import patch

# Initialize TestClient
client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint to ensure it serves the index.html interface."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<title>" in response.text

@patch("main.analyze_email")
def test_process_email_refund(mock_analyze):
    """Test processing a refund email with mocked Gemini response."""
    # Define mock return value
    mock_analyze.return_value = EmailAnalysis(
        intent=Intent.REFUND,
        urgency="HIGH",
        entities=["Order #98765", "Jane Smith"],
        summary="Customer Jane Smith is asking for a refund on order #98765.",
        suggested_action="Verify order status and initiate refund."
    )
    
    payload = {
        "subject": "Need help with my order",
        "body": "Hello, I am Jane Smith. I'd like to return my item from order #98765. It was broken."
    }
    
    response = client.post("/process-email", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "REFUND"
    assert data["urgency"] == "HIGH"
    assert "Order #98765" in data["entities"]
    mock_analyze.assert_called_once()

@patch("main.analyze_email")
def test_process_email_tech_support(mock_analyze):
    """Test processing a tech support email with mocked Gemini response."""
    mock_analyze.return_value = EmailAnalysis(
        intent=Intent.TECH_SUPPORT,
        urgency="MEDIUM",
        entities=["Error Code 500", "Login Page"],
        summary="User is experiencing a 500 error on the login page.",
        suggested_action="Assign to DevOps for investigation."
    )
    
    payload = {
        "subject": "Cannot login",
        "body": "I am getting an Error Code 500 when I try to access the login page. Please help."
    }
    
    response = client.post("/process-email", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "TECH_SUPPORT"
    assert "Error Code 500" in data["entities"]

def test_process_email_invalid_payload():
    """Test the endpoint with missing required fields."""
    payload = {
        "subject": "Missing body"
    }
    response = client.post("/process-email", json=payload)
    assert response.status_code == 422 # Unprocessable Entity
