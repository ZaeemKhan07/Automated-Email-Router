# Automated Email Router

An intelligent backend webhook that classifies emails and extracts entities using **FastAPI** and **Gemini 2.5 Flash-Lite**.

## 🚀 Overview

The Automated Email Router is designed to streamline customer support workflows by automatically analyzing incoming emails. It identifies the user's intent, extracts critical information (like order numbers and names), determines urgency, and simulates routing to the appropriate department.

### Key Features
- **AI-Powered Classification:** Uses Gemini 2.5 Flash-Lite for low-latency, high-accuracy intent detection.
- **Structured Data Extraction:** Leverages Pydantic models and Gemini's JSON schema mode to ensure consistent API responses.
- **Urgency Detection:** Flags high-priority requests (e.g., "Critical" or "High") for immediate action.
- **Simulation Routing:** Includes logic to "route" emails to Billing, Tech Support, Sales, or Feedback teams.
- **Fully Tested:** Includes a suite of automated tests with mocked LLM responses.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **LLM:** Gemini 2.5 Flash-Lite (`gemini-2.5-flash-lite`)
- **SDK:** `google-genai` (v2.7.0+)
- **Validation:** Pydantic v2
- **Testing:** Pytest & HTTPX

---

## 📋 Prerequisites

- Python 3.10 or higher
- A Gemini API Key (obtained from [Google AI Studio](https://aistudio.google.com/))

---

## ⚙️ Installation & Setup

1. **Clone or navigate to the project directory:**
   ```powershell
   cd "Automated Email Router"
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Open the `.env` file and replace `your_api_key_here` with your actual Gemini API key:
   ```text
   GEMINI_API_KEY=your_actual_api_key_here
   ```

---

## 🏃 Running the System

### 1. Start the FastAPI Server
Run the server using `uvicorn`:
```powershell
python -m uvicorn main:app --reload
```
The API will be available at: `http://127.0.0.1:8000`

### 2. Access API Documentation
Once the server is running, you can view the interactive Swagger UI at:
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Usage Examples

### Process an Email (cURL)
```bash
curl -X POST "http://127.0.0.1:8000/process-email" \
     -H "Content-Type: application/json" \
     -d '{
           "subject": "Broken item in order #55432",
           "body": "Hello, I am John Doe. I received my order #55432 today but it is damaged. I would like a refund please."
         }'
```

### Expected Response
```json
{
  "intent": "REFUND",
  "urgency": "HIGH",
  "entities": ["order #55432", "John Doe"],
  "summary": "John Doe is requesting a refund for a damaged item in order #55432.",
  "suggested_action": "Verify damage with customer and initiate refund process."
}
```

---

## ✅ Running Tests

The project includes automated tests to ensure the routing logic and API schema remain intact.

```powershell
python -m pytest tests/test_emails.py
```

---

## 📂 Project Structure

```text
automated-email-router/
├── main.py                # FastAPI entry point & simulated routing logic
├── models.py              # Pydantic schemas (Request/Response)
├── services/
│   └── gemini_service.py  # Gemini 2.5 Flash-Lite integration
├── tests/
│   └── test_emails.py     # Automated test suite
├── .env                   # Configuration (API Keys)
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```
