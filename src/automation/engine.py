from typing import Any, Dict
from src.automation.rules import RuleConditionNode, ASTRule, RuleActionNode

class ConditionEvaluator:
    @classmethod
    def evaluate(cls, node: RuleConditionNode, context: Dict[str, Any]) -> bool:
        if node.operator == "AND":
            if not node.children: return True
            return all(cls.evaluate(child, context) for child in node.children)
            
        elif node.operator == "OR":
            if not node.children: return False
            return any(cls.evaluate(child, context) for child in node.children)
            
        elif node.operator == "EQUALS":
            ctx_val = context.get(node.field)
            # handle case-insensitive string compare
            if isinstance(ctx_val, str) and isinstance(node.value, str):
                return ctx_val.lower() == node.value.lower()
            return ctx_val == node.value
            
        elif node.operator == "CONTAINS":
            ctx_val = context.get(node.field)
            if not isinstance(ctx_val, str) or not isinstance(node.value, str): return False
            return node.value.lower() in ctx_val.lower()
            
        elif node.operator == "GREATER_THAN":
            ctx_val = context.get(node.field)
            if ctx_val is None or node.value is None: return False
            try:
                return float(ctx_val) > float(node.value)
            except (ValueError, TypeError):
                return False
                
        return False

class ActionExecutor:
    @classmethod
    def execute(cls, actions: list[RuleActionNode], context: Dict[str, Any]) -> Dict[str, Any]:
        mutated_context = dict(context)
        for action in actions:
            if action.action_type == "SET_CATEGORY":
                mutated_context["category"] = action.payload.get("category_id")
            elif action.action_type == "SET_TAG":
                tags = mutated_context.get("tags", [])
                tags.append(action.payload.get("tag"))
                mutated_context["tags"] = tags
        return mutated_context

class WorkflowEngine:
    @classmethod
    def run_synchronous_rules(cls, rules: list[ASTRule], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes an array of AST rules against a context object.
        Rules are evaluated in priority order.
        """
        # Sort by priority
        rules = sorted(rules, key=lambda x: x.priority)
        current_context = dict(context)
        
        for rule in rules:
            if ConditionEvaluator.evaluate(rule.condition_ast, current_context):
                current_context = ActionExecutor.execute(rule.actions, current_context)
                
        return current_context
