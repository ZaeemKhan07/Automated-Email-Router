from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

class Intent(str, Enum):
    REFUND = "REFUND"
    TECH_SUPPORT = "TECH_SUPPORT"
    SALES = "SALES"
    OTHER = "OTHER"

class EmailPayload(BaseModel):
    subject: str
    body: str

class EmailAnalysis(BaseModel):
    intent: Intent
    urgency: str = Field(description="Urgency level: LOW, MEDIUM, HIGH, CRITICAL")
    entities: List[str] = Field(description="Extracted entities like order numbers, names, product names")
    summary: str
    suggested_action: str
