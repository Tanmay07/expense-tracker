from execution_policy.application.services import ASTEvaluator
from execution_policy.domain.models import PolicyContext, RuleAST, RuleOperator


def test_ast_evaluator_eq():
    context = PolicyContext(
        request_id="req_1",
        decision_metadata={"amount": 500},
        capability_metadata={"automation_level": "FULLY_AUTOMATED"},
        user_metadata={},
        risk_profile={},
    )

    ast = RuleAST(operator=RuleOperator.EQ, field="decision_metadata.amount", value=500)
    assert ASTEvaluator.evaluate(ast, context) is True

    ast_false = RuleAST(
        operator=RuleOperator.EQ, field="decision_metadata.amount", value=1000
    )
    assert ASTEvaluator.evaluate(ast_false, context) is False


def test_ast_evaluator_gt():
    context = PolicyContext(
        request_id="req_2",
        decision_metadata={"amount": 5000},
        capability_metadata={},
        user_metadata={},
        risk_profile={},
    )

    ast = RuleAST(
        operator=RuleOperator.GT, field="decision_metadata.amount", value=1000
    )
    assert ASTEvaluator.evaluate(ast, context) is True


def test_ast_evaluator_and():
    context = PolicyContext(
        request_id="req_3",
        decision_metadata={"amount": 5000},
        capability_metadata={"risk_level": "HIGH"},
        user_metadata={},
        risk_profile={},
    )

    ast = RuleAST(
        operator=RuleOperator.AND,
        conditions=[
            RuleAST(
                operator=RuleOperator.GT, field="decision_metadata.amount", value=1000
            ),
            RuleAST(
                operator=RuleOperator.EQ,
                field="capability_metadata.risk_level",
                value="HIGH",
            ),
        ],
    )
    assert ASTEvaluator.evaluate(ast, context) is True
