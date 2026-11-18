from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from llm import LLMWrapper


app = FastAPI()


# Create LLM wrapper
llm = LLMWrapper()


# Dependency
def get_app_info():
    return {
        "service": "Task Management AI API",
        "version": "1.0"
    }


# Request model
class ChatRequest(BaseModel):
    message: str


# Response model
class ChatResponse(BaseModel):
    answer: str


# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Path parameter + query parameter
@app.get("/tickets/{ticket_id}")
def get_ticket(
    ticket_id: int,
    priority: str = "MEDIUM"
):
    return {
        "ticket_id": ticket_id,
        "priority": priority
    }


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    app_info: dict = Depends(get_app_info)
):

    # Check for empty message
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    # Call Gemini
    answer = llm.generate(request.message)

    return {
        "answer": answer
    }