from pydantic import BaseModel
from typing import Optional

class GenerateRequest(BaseModel):
    """Request model for cover letter generation"""
    job_description: str
    resume: str
    api_key: Optional[str] = None
    model_provider: str = "openai"

    class Config:
        schema_extra = {
            "example": {
                "job_description": "Software Engineer position...",
                "resume": "John Doe\nSoftware Engineer...",
                "api_key": "your-api-key",
                "model_provider": "openai"
            }
        } 