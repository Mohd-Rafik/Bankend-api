from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.onboarding import router as onboarding_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(onboarding_router)


@app.get("/")
def home():
    return {"status": "success", "message": "API Running", "data": None}
