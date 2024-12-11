from fastapi import FastAPI
from router.quality_router import router as quality_router
from router.aqi_router import router as aqi_router
from router.alert_router import router as alert_router

app = FastAPI()

app.include_router(quality_router, prefix="/quality", tags=["quality"])
app.include_router(aqi_router, prefix="/aqi", tags=["aqi"])
app.include_router(alert_router, prefix="/alert", tags=["alert"])
