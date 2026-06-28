import pytest
from src.automation.rules import RuleConditionNode, ASTRule, RuleActionNode
from src.automation.engine import ConditionEvaluator, WorkflowEngine

def test_ast_condition_evaluator_simple_equals():
    node = RuleConditionNode(operator="EQUALS", field="merchant", value="Starbucks")
    
    assert ConditionEvaluator.evaluate(node, {"merchant": "Starbucks"}) == True
    assert ConditionEvaluator.evaluate(node, {"merchant": "Amazon"}) == False
    assert ConditionEvaluator.evaluate(node, {"merchant": "STARBUCKS"}) == True # Case insensitive

def test_ast_condition_evaluator_greater_than():
    node = RuleConditionNode(operator="GREATER_THAN", field="amount", value=50.0)
    
    assert ConditionEvaluator.evaluate(node, {"amount": 100.0}) == True
    assert ConditionEvaluator.evaluate(node, {"amount": 20.0}) == False
    assert ConditionEvaluator.evaluate(node, {"amount": "75.5"}) == True

def test_ast_condition_evaluator_nested_and_or():
    # Rule: IF (merchant == "Amazon" OR merchant == "Flipkart") AND (amount > 1000)
    node = RuleConditionNode(
        operator="AND",
        children=[
            RuleConditionNode(
                operator="OR",
                children=[
                    RuleConditionNode(operator="EQUALS", field="merchant", value="Amazon"),
                    RuleConditionNode(operator="EQUALS", field="merchant", value="Flipkart"),
                ]
            ),
            RuleConditionNode(operator="GREATER_THAN", field="amount", value=1000.0)
        ]
    )
    
    # 1. Matches Amazon & High Amount
    assert ConditionEvaluator.evaluate(node, {"merchant": "Amazon", "amount": 1500}) == True
    
    # 2. Matches Flipkart & High Amount
    assert ConditionEvaluator.evaluate(node, {"merchant": "Flipkart", "amount": 1200}) == True
    
    # 3. Fails: Amazon but low amount
    assert ConditionEvaluator.evaluate(node, {"merchant": "Amazon", "amount": 500}) == False
    
    # 4. Fails: Starbucks but high amount
    assert ConditionEvaluator.evaluate(node, {"merchant": "Starbucks", "amount": 2000}) == False

def test_workflow_engine():
    # Define an AST Rule
    ast_rule = ASTRule(
        id="rule_123",
        priority=10,
        condition_ast=RuleConditionNode(
            operator="CONTAINS", field="merchant", value="Netflix"
        ),
        actions=[
            RuleActionNode(action_type="SET_CATEGORY", payload={"category_id": "Entertainment"}),
            RuleActionNode(action_type="SET_TAG", payload={"tag": "Subscription"})
        ]
    )
    
    context = {
        "merchant": "Netflix Subscription",
        "amount": 15.99,
        "tags": []
    }
    
    mutated_ctx = WorkflowEngine.run_synchronous_rules([ast_rule], context)
    
    assert mutated_ctx["category"] == "Entertainment"
    assert "Subscription" in mutated_ctx["tags"]
