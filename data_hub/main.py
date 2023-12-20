from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data_hub.routes.dashboard import dashboard_router
from data_hub.routes.onboarding import onboarding_router
from data_hub.routes.ai import ai_router

app = FastAPI()

origins = ["https://app.namora.ai", "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health_check")
async def health_check():
    return {"status": "All Ok"}


app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(onboarding_router, prefix="/onboarding", tags=["Onboarding"])
app.include_router(ai_router, prefix="/ai", tags=["AI"])
