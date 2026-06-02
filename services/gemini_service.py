import os
from google import genai
from dotenv import load_dotenv
from models import EmailPayload, EmailAnalysis

# Load environment variables
load_dotenv()

# Initialize the Gemini client
# API Key should be in .env as GEMINI_API_KEY
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_email(payload: EmailPayload) -> EmailAnalysis:
    """
    Uses Gemini 2.5 Flash-Lite to analyze email content and return structured data.
    """
    prompt = f"""
    Analyze the following email and extract structured information according to the schema.
    
    Subject: {payload.subject}
    Body: {payload.body}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': EmailAnalysis,
            }
        )
        
        if not response.parsed:
            raise ValueError("Failed to parse response from Gemini or response was empty.")
            
        return response.parsed
        
    except Exception as e:
        # In a real application, you would use a logger here
        print(f"Error calling Gemini Service: {e}")
        raise e
