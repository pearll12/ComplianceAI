from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.policy import router as policy_router

app = FastAPI(title="ComplianceAI", version="1.0")

# Allow your frontend (Vite default) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "ComplianceAI backend running"}

# API routes
app.include_router(policy_router, prefix="/api")