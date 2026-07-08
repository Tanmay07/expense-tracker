from sqlalchemy.orm import Session
from typing import List, Optional

from .database import (
    ConversationModel,
    MessageModel,
    MemoryItemModel,
    PromptTemplateModel,
    AgentDefinitionModel,
)
from ..domain.models import (
    Conversation,
    Message,
    MemoryItem,
    PromptTemplate,
    AgentDefinition,
)


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db


class ConversationRepository(BaseRepository):
    def get_by_id(self, conversation_id: str) -> Optional[Conversation]:
        record = (
            self.db.query(ConversationModel)
            .filter(ConversationModel.id == conversation_id)
            .first()
        )
        if not record:
            return None

        messages = (
            self.db.query(MessageModel)
            .filter(MessageModel.conversation_id == conversation_id)
            .order_by(MessageModel.timestamp)
            .all()
        )

        conv = Conversation(
            id=record.id,
            user_id=record.user_id,
            started_at=record.started_at,
            updated_at=record.updated_at,
            context_summaries=record.context_summaries,
            messages=[Message(**m.__dict__) for m in messages],
        )
        return conv

    def save(self, conversation: Conversation) -> Conversation:
        # Save or update conversation
        conv_record = ConversationModel(
            id=conversation.id,
            user_id=conversation.user_id,
            started_at=conversation.started_at,
            updated_at=conversation.updated_at,
            context_summaries=conversation.context_summaries,
        )
        self.db.merge(conv_record)

        # Save messages
        for msg in conversation.messages:
            msg_record = MessageModel(
                id=msg.id,
                conversation_id=conversation.id,
                role=msg.role.value,
                content=msg.content,
                timestamp=msg.timestamp,
                name=msg.name,
                tool_calls=msg.tool_calls,
                explainability_metadata=msg.explainability_metadata,
            )
            self.db.merge(msg_record)

        self.db.commit()
        return conversation


class MemoryRepository(BaseRepository):
    def get_by_user_id(self, user_id: str) -> List[MemoryItem]:
        records = (
            self.db.query(MemoryItemModel)
            .filter(MemoryItemModel.user_id == user_id)
            .all()
        )
        return [MemoryItem(**r.__dict__) for r in records]

    def save(
        self, memory: MemoryItem, embedding: Optional[List[float]] = None
    ) -> MemoryItem:
        record_data = memory.model_dump()
        record_data["type"] = memory.type.value  # handle enum
        if embedding:
            record_data["embedding"] = embedding

        record = MemoryItemModel(**record_data)
        self.db.merge(record)
        self.db.commit()
        return memory


class PromptRepository(BaseRepository):
    def get_by_name(self, name: str) -> Optional[PromptTemplate]:
        # Get the latest version
        record = (
            self.db.query(PromptTemplateModel)
            .filter(PromptTemplateModel.name == name)
            .order_by(PromptTemplateModel.version.desc())
            .first()
        )
        if record:
            return PromptTemplate(**record.__dict__)
        return None

    def save(self, prompt: PromptTemplate) -> PromptTemplate:
        record = PromptTemplateModel(**prompt.model_dump())
        self.db.merge(record)
        self.db.commit()
        return prompt


class AgentRepository(BaseRepository):
    def get_by_name(self, name: str) -> Optional[AgentDefinition]:
        record = (
            self.db.query(AgentDefinitionModel)
            .filter(AgentDefinitionModel.name == name)
            .first()
        )
        if record:
            return AgentDefinition(**record.__dict__)
        return None
