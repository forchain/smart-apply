from fastapi import APIRouter, HTTPException
from ..core.generator import CoverLetterGenerator
from ..core.config import Config
from ..models.request import GenerateRequest

router = APIRouter()

@router.post("/generate",
    response_model=dict,
    summary="Generate Cover Letter")
async def generate_cover_letter(request: GenerateRequest):
    try:
        generator = CoverLetterGenerator(request.api_key, request.provider)
        cover_letter = generator.generate(request.job_description, request.resume)
        return {"cover_letter": cover_letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/config/{provider}",
    response_model=dict,
    summary="Get Provider Config")
async def get_provider_config(provider: str):
    config = Config()
    return {
        "api_key": config.get_api_key(provider),
        "model": config.get_model(provider),
        "base_url": config.get_base_url(provider)
    }

@router.get("/health",
    response_model=dict,
    summary="Health Check")
async def health_check():
    return {"status": "healthy"} 