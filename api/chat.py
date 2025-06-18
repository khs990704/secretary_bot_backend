from fastapi import APIRouter
from schemas.chat import ChatRequest, ChatResponse
from services.model import generate_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    reply = generate_response(request.message)

    return ChatResponse(reply=reply)