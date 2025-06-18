from fastapi import APIRouter
from schemas.chat import ChatRequest, ChatResponse
from services.model import call_model
from api.tools.mcp_agent import process_function_call

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    raw_response = call_model(req.message)
    final_response = process_function_call(raw_response)
    return ChatResponse(response=final_response)