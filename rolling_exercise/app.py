from fastapi import FastAPI
from router.quality_router import router as quality_router

app = FastAPI()

app.include_router(quality_router, prefix="/quality", tags=["quality"])
