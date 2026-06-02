from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from models import EmailPayload, EmailAnalysis, Intent
from services.gemini_service import analyze_email
import os

app = FastAPI(
    title="Automated Email Router",
    description="An API that classifies and extracts entities from emails using Gemini 2.5 Flash-Lite."
)

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
async def root():
    """
    Serve the index.html file as the root interface.
    """
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.post("/process-email", response_model=EmailAnalysis)
async def process_email(payload: EmailPayload):
    """
    Endpoint to process raw email data.
    - Classifies intent
    - Extracts entities
    - Determines urgency
    - Suggests an action
    """
    try:
        # 1. Analyze email using Gemini Service
        analysis = analyze_email(payload)
        
        # 2. Route based on extracted intent (Simulation)
        route_to_department(analysis)
        
        return analysis
    except Exception as e:
        # Log the error details here
        print(f"Error processing email: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while processing the email with Gemini."
        )

def route_to_department(analysis: EmailAnalysis):
    """
    Simulates routing logic based on the extracted intent and urgency.
    """
    intent = analysis.intent
    urgency = analysis.urgency
    
    print(f"\n--- ROUTING NOTIFICATION ---")
    print(f"Intent: {intent}")
    print(f"Urgency: {urgency}")
    print(f"Summary: {analysis.summary}")
    
    if intent == Intent.REFUND:
        print("ACTION: Triggered Refund Workflow (Billing Dept notified)")
    elif intent == Intent.TECH_SUPPORT:
        print("ACTION: Created Ticket in ZenDesk (Technical Support Queue)")
    elif intent == Intent.SALES:
        print("ACTION: Forwarded to Salesforce (Sales Team notified)")
    else:
        print("ACTION: Routed to General Customer Service Inbox")
    
    if urgency in ["HIGH", "CRITICAL"]:
        print("ALERT: This request has been flagged for IMMEDIATE attention!")
    print(f"----------------------------\n")
