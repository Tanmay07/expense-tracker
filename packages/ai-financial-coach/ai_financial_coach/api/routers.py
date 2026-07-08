from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from .dependencies import get_coach_service
from ..application.services import CoachService
from ..domain.models import Message

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    conversation_id: str
    content: str

@router.post("/chat", response_model=Message)
def chat(
    request: ChatRequest,
    coach_service: CoachService = Depends(get_coach_service)
):
    try:
        response_message = coach_service.process_message(
            request.conversation_id, request.user_id, request.content
        )
        return response_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
