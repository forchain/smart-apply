from pydantic import BaseModel, ConfigDict

class GenerateRequest(BaseModel):
    job_description: str
    resume: str
    api_key: str
    provider: str = "openai"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "job_description": "Software Engineer position...",
                "resume": "John Doe\nSoftware Engineer...",
                "api_key": "your-api-key",
                "provider": "openai"
            }
        }
    ) 