from fastapi import APIRouter, HTTPException
from ..core.generator import CoverLetterGenerator
from ..models.request import GenerateRequest
import logging

router = APIRouter()

@router.post("/generate")
async def generate_cover_letter(request: GenerateRequest):
    try:
        # Print request data for debugging
        print("Received Request:")
        print(request.dict())

        generator = CoverLetterGenerator(
            request.api_key, 
            request.provider,
            request.language,
            request.example
        )
        result = generator.generate(
            request.job_description, 
            request.resume,
            request.enable_fact_check  # Add fact check flag
        )
        if not result:
            raise ValueError("Failed to generate cover letter")
            
        return result
    except Exception as e:
        logging.error(f"Error in generate_cover_letter: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/health",
    response_model=dict,
    summary="Health Check")
async def health_check():
    return {"status": "healthy"} 