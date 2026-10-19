import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

app = FastAPI(title="ZETA AI")

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "app": "ZETA AI",
        "status": "online",
        "message": "Hello! I am ZETA."
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    if not client:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured."
        )

    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=(
                "You are ZETA, a friendly AI assistant with a warm, "
                "feminine conversational style. You help with questions, "
                "learning, and programming. You are an AI, not a human.\n\n"
                + request.message
            )
        )

        return {"reply": response.text or "Please try again."}

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Gemini request failed. Check the service configuration."
)
