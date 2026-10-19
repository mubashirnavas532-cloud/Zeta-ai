from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ZETA AI")


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
    message = request.message.strip()

    if not message:
        return {"reply": "Please tell me something!"}

    return {
        "reply": (
            f"Hello! I'm ZETA. You said: {message}. "
            "My advanced AI brain will be connected soon!"
        )
    }
