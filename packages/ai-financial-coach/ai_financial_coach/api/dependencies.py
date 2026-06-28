from fastapi import Depends
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.repositories import ConversationRepository, MemoryRepository, PromptRepository
from ..application.orchestration import AgentCoordinatorService, ContextService, ExplainabilityService
from ..application.services import CoachService

def get_conversation_repo(db: Session = Depends(get_db)):
    return ConversationRepository(db)
    
def get_coach_service(
    conversation_repo: ConversationRepository = Depends(get_conversation_repo)
) -> CoachService:
    coordinator = AgentCoordinatorService()
    context_service = ContextService()
    explain_service = ExplainabilityService()
    return CoachService(conversation_repo, coordinator, context_service, explain_service)
