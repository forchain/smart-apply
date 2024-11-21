from pydantic import BaseModel, ConfigDict
from typing import Optional

class GenerateRequest(BaseModel):
    job_description: str
    resume: str
    api_key: str
    provider: str = "openai"
    language: str = "zh"
    example: str = ""
    enable_fact_check: bool = False

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "job_description": "Software Engineer position...",
                "resume": "Tony Zhou\nSoftware Engineer...",
                "api_key": "your-api-key",
                "provider": "openai",
                "language": "zh",
                "example": "",
                "enable_fact_check": False
            }
        }
    ) 