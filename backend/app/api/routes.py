from fastapi import APIRouter, HTTPException
from ..core.generator import CoverLetterGenerator
from ..models.request import GenerateRequest

router = APIRouter()

@router.post("/generate")
async def generate_cover_letter(request: GenerateRequest):
    try:
        generator = CoverLetterGenerator(request.api_key, request.provider)
        cover_letter = generator.generate(request.job_description, request.resume)
        if not cover_letter:
            raise ValueError("Failed to generate cover letter")
        return {"cover_letter": cover_letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/health",
    response_model=dict,
    summary="Health Check")
async def health_check():
    return {"status": "healthy"} 