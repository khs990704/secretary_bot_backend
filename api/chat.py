from fastapi import APIRouter
from schemas.chat import ChatRequest, ChatResponse
from services.model import generate_response
# from services.model import stream_response
# from fastapi.responses import StreamingResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    reply = generate_response(request.message)

    return ChatResponse(reply=reply)

# @router.post("/chat")
# async def chat_endpoint(request: ChatRequest):
#     body = await request.json()
#     message = body.get("message", "")
#
#     return StreamingResponse(stream_response(message), media_type="text/plain")