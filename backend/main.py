from fastapi import FastAPI
from app.api.routes import router
import uvicorn

app = FastAPI(
    title="Smart Apply API",
    description="API for generating cover letters using AI models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 