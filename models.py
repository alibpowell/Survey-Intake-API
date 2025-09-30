from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator
import hashlib

def hash_value(value: str) -> str:
    """Return SHA-256 hash of a string."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    consent: bool = Field(..., description="Must be true to accept")
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=1000)
    user_agent: Optional[str] = None          # optional
    submission_id: Optional[str] = None       # optional, auto-generated later

    @validator("comments")
    def _strip_comments(cls, v):
        return v.strip() if isinstance(v, str) else v

    @validator("consent")
    def _must_consent(cls, v):
        if v is not True:
            raise ValueError("consent must be true")
        return v

    def hashed_record(self) -> dict:
        """
        Return a dictionary version of this submission with PII hashed.
        Only email and age are hashed.
        """
        return {
            "name": self.name,
            "email": hash_value(self.email),
            "age": hash_value(str(self.age)),
            "consent": self.consent,
            "rating": self.rating,
            "comments": self.comments,
            "user_agent": self.user_agent,
            "submission_id": self.submission_id
        }

class StoredSurveyRecord(SurveySubmission):
    received_at: datetime
    ip: str


