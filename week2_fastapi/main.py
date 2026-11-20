from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx

from llm import LLMWrapper

from db import (
    init_db,
    create_session,
    session_exists,
    save_message,
    get_messages,
    get_session_summary,
    update_session_summary
)


app = FastAPI()

llm = LLMWrapper()


# Learning-purpose context limits
MAX_CONTEXT_TOKENS = 500
LAST_N_MESSAGES = 4


# Initialize SQLite database
init_db()


def get_app_info():
    return {
        "service": "Task Management AI API",
        "version": "1.0"
    }


class ChatRequest(BaseModel):
    message: str
    session_id: int | None = None


class ChatResponse(BaseModel):
    session_id: int
    answer: str


class SessionResponse(BaseModel):
    session_id: int


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/tickets/{ticket_id}")
def get_ticket(
    ticket_id: int,
    priority: str = "MEDIUM"
):
    return {
        "ticket_id": ticket_id,
        "priority": priority
    }


@app.post("/sessions", response_model=SessionResponse)
def create_new_session():
    session_id = create_session()

    return {
        "session_id": session_id
    }


def estimate_tokens(text: str) -> int:
    """
    Learning-purpose token estimation.

    Rough assumption:
    1 token ≈ 4 characters.
    """

    return max(1, len(text) // 4)


def format_messages(messages):
    formatted = []

    for message in messages:
        formatted.append(
            f"{message['role']}: {message['content']}"
        )

    return "\n".join(formatted)


def build_context(session_id: int):

    summary = get_session_summary(session_id)

    messages = get_messages(session_id)

    # Keep only recent messages
    recent_messages = messages[-LAST_N_MESSAGES:]

    # Older messages can be summarised
    old_messages = messages[:-LAST_N_MESSAGES]

    context_parts = []

    if summary:
        context_parts.append(
            f"Conversation summary:\n{summary}"
        )

    if recent_messages:
        context_parts.append(
            "Recent conversation:\n"
            + format_messages(recent_messages)
        )

    context = "\n\n".join(context_parts)

    estimated_tokens = estimate_tokens(context)

    # Context is within the limit
    if estimated_tokens <= MAX_CONTEXT_TOKENS:
        return context

    # Context is too large
    if old_messages:

        old_conversation = format_messages(
            old_messages
        )

        new_summary = llm.summarize(
            old_conversation
        )

        update_session_summary(
            session_id,
            new_summary
        )

        context_parts = []

        context_parts.append(
            f"Conversation summary:\n{new_summary}"
        )

        context_parts.append(
            "Recent conversation:\n"
            + format_messages(recent_messages)
        )

        context = "\n\n".join(context_parts)

    # Final safety limit
    if estimate_tokens(context) > MAX_CONTEXT_TOKENS:

        context = context[-(MAX_CONTEXT_TOKENS * 4):]

    return context


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

    # Create a new session if no session_id is provided
    if request.session_id is None:

        session_id = create_session()

    else:

        session_id = request.session_id

        if not session_exists(session_id):
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )

    # Save user's message
    save_message(
        session_id,
        "user",
        request.message
    )

    # Build conversation context
    context = build_context(session_id)

    prompt = f"""
You are an AI assistant for a Task Management AI API.

Use the conversation context below to answer the
latest user message.

Conversation context:
{context}

Latest user message:
{request.message}
"""

    answer = llm.generate(prompt)

    # Save AI response
    save_message(
        session_id,
        "assistant",
        answer
    )

    return {
        "session_id": session_id,
        "answer": answer
    }


@app.get("/sessions/{session_id}")
def get_session(session_id: int):

    if not session_exists(session_id):
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return {
        "session_id": session_id,
        "summary": get_session_summary(session_id),
        "messages": get_messages(session_id)
    }


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

            for chunk in llm.generate_stream(
                chat_request.message
            ):

                if await request.is_disconnected():

                    print("Client disconnected.")

                    return

                if chunk:

                    yield f"data: {chunk}\n\n"

        except Exception as error:

            print(f"Streaming error: {error}")

            yield "data: [ERROR] Streaming request failed.\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@app.get("/timeout-test")
async def timeout_test():

    timeout = httpx.Timeout(1.0)

    try:

        async with httpx.AsyncClient(
            timeout=timeout
        ) as client:

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