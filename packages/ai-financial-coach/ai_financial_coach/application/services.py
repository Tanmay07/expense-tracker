from ..domain.models import Conversation, Message, Role, MemoryItem
from ..infrastructure.repositories import ConversationRepository, MemoryRepository, PromptRepository
from .orchestration import AgentCoordinatorService, ContextService, ExplainabilityService

class CoachService:
    def __init__(
        self,
        conversation_repo: ConversationRepository,
        coordinator: AgentCoordinatorService,
        context_service: ContextService,
        explain_service: ExplainabilityService
    ):
        self.conversation_repo = conversation_repo
        self.coordinator = coordinator
        self.context_service = context_service
        self.explain_service = explain_service

    def process_message(self, conversation_id: str, user_id: str, content: str) -> Message:
        conversation = self.conversation_repo.get_by_id(conversation_id)
        if not conversation:
            conversation = Conversation(id=conversation_id, user_id=user_id)
            
        user_message = Message(role=Role.USER, content=content)
        conversation.messages.append(user_message)
        
        # 1. Build Context
        context = self.context_service.build_context(user_id, content)
        
        # 2. Select Agent
        agent = self.coordinator.route_query(content)
        
        # 3. Generate Response
        response_text = agent.run(conversation.messages, context)
        
        # 4. Generate Explainability
        explanation = self.explain_service.generate_explanation(response_text, context)
        
        assistant_message = Message(
            role=Role.ASSISTANT, 
            content=response_text,
            explainability_metadata=explanation
        )
        conversation.messages.append(assistant_message)
        
        # Save state
        self.conversation_repo.save(conversation)
        
        return assistant_message

class MemoryService:
    def __init__(self, repo: MemoryRepository):
        self.repo = repo
        
    def add_memory(self, item: MemoryItem):
        # In a real app, generate embedding here before saving
        return self.repo.save(item)

class PromptService:
    def __init__(self, repo: PromptRepository):
        self.repo = repo
        
    def get_prompt(self, name: str):
        return self.repo.get_by_name(name)
