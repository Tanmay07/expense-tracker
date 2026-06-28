from typing import Any, List, Optional, Union
from pydantic import BaseModel, Field

class RuleConditionNode(BaseModel):
    # This acts as the base JSON AST node
    operator: str # "AND", "OR", "EQUALS", "CONTAINS", "GREATER_THAN"
    field: Optional[str] = None # e.g. "amount", "merchant"
    value: Optional[Any] = None # e.g. 500.0, "Starbucks"
    children: Optional[List['RuleConditionNode']] = None # For AND/OR

class RuleActionNode(BaseModel):
    action_type: str # "SET_CATEGORY", "TRIGGER_WEBHOOK"
    payload: dict

class ASTRule(BaseModel):
    id: str
    priority: int
    condition_ast: RuleConditionNode
    actions: List[RuleActionNode]
