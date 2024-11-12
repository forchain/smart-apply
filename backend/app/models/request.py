from pydantic import BaseModel, ConfigDict
from typing import Optional

class GenerateRequest(BaseModel):
    """Request model for cover letter generation"""
    job_description: str
    resume: str
    api_key: Optional[str] = None
    provider: str = "openai"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "job_description": "Software Engineer position...",
                "resume": "John Doe\nSoftware Engineer...",
                "api_key": "your-api-key",
                "provider": "openai"
            }
        },
        protected_namespaces=()
    ) 