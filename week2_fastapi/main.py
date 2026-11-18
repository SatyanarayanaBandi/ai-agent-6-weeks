from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx

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


# Normal chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    app_info: dict = Depends(get_app_info)
):
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    answer = llm.generate(request.message)

    return {
        "answer": answer
    }


# Streaming chat endpoint
@app.post("/chat/stream")
async def chat_stream(
    request: Request,
    chat_request: ChatRequest
):
    if not chat_request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    async def generate():
        try:
            # Gemini SDK provides a synchronous streaming iterator.
            for chunk in llm.generate_stream(chat_request.message):

                # Stop generating if the client disconnects.
                if await request.is_disconnected():
                    print("Client disconnected.")
                    return

                if chunk:
                    # Server-Sent Events format
                    yield f"data: {chunk}\n\n"

        except Exception as error:
            print(f"Streaming error: {error}")
            yield "data: [ERROR] Streaming request failed.\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


# HTTPX timeout demonstration
@app.get("/timeout-test")
async def timeout_test():
    timeout = httpx.Timeout(1.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                "https://httpbin.org/delay/3"
            )

            return {
                "status": response.status_code,
                "message": "Request completed within timeout"
            }

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=408,
            detail="Upstream request timed out"
        )