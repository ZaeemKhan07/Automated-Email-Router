# GEMINI.md - Project Instructions

## Project Overview
**Automated Email Router** is a FastAPI-based intelligent webhook that automates the classification and entity extraction of incoming emails. It leverages **Gemini 2.5 Flash-Lite** to provide low-latency, structured analysis of customer queries.

### Core Technologies
- **Framework:** FastAPI
- **LLM:** Gemini 2.5 Flash-Lite (`gemini-2.5-flash-lite`)
- **SDK:** `google-genai` (Unified SDK)
- **Validation:** Pydantic v2
- **Testing:** Pytest & HTTPX

### Architecture
- `main.py`: The entry point for the FastAPI application. It contains the `/process-email` endpoint and the `route_to_department` logic which simulates business workflows based on AI classification.
- `models.py`: Defines the source of truth for data structures (`EmailPayload`, `EmailAnalysis`) and the `Intent` Enum.
- `services/gemini_service.py`: Encapsulates the interaction with the Google GenAI SDK. It uses structured output mode to ensure Gemini returns valid JSON matching the `EmailAnalysis` schema.
- `tests/`: Contains automated unit tests. External LLM calls are mocked to ensure reliable and fast testing.

---

## Building and Running

### Prerequisites
- Python 3.10+
- `.env` file with `GEMINI_API_KEY` defined.

### Setup
```powershell
# Install dependencies
pip install -r requirements.txt
```

### Execution
```powershell
# Start the FastAPI server
python -m uvicorn main:app --reload
```
- **API Docs:** Access Swagger UI at `http://127.0.0.1:8000/docs`

### Testing
```powershell
# Run all tests
python -m pytest tests/test_emails.py
```

---

## Development Conventions

### 1. Structured AI Outputs
Always use the `google-genai` SDK's structured output capability. When modifying the `EmailAnalysis` model, ensure the `analyze_email` function in `services/gemini_service.py` is updated to reflect any critical prompt changes or schema requirements.

### 2. Type Safety
Maintain strict type safety by using Pydantic models for all API request and response bodies. Define Enums for categorical data (like `Intent` or `Urgency`) to prevent runtime errors.

### 3. Testing Standard
Any new feature or routing logic MUST be accompanied by a test case in `tests/test_emails.py`. Use `@patch("main.analyze_email")` to mock the Gemini service response to ensure tests are deterministic and do not consume API quota.

### 4. Error Handling
LLM calls should be wrapped in try-except blocks. If the LLM fails, the API should return a descriptive `500 HTTPException` while logging the raw error for internal debugging.
