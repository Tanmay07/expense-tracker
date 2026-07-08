from typing import Dict, List, Optional
from .models import AgentDefinition, AgentRole, MemoryScope

class AgentRegistryService:
    """
    Central registry for all Cognitive Agents in PFOS.
    No independent governance; capabilities and policies are centrally managed.
    """
    def __init__(self):
        self._agents: Dict[AgentRole, AgentDefinition] = {}
        self._initialize_registry()

    def _initialize_registry(self):
        self.register(AgentDefinition(
            id="agent_supervisor_01",
            role=AgentRole.SUPERVISOR,
            capabilities=["orchestration", "conflict_resolution", "final_approval", "delegation"],
            allowed_tools=["delegate_to_agent", "request_human_approval", "query_knowledge_graph"],
            memory_scope=MemoryScope.LONG_TERM,
            escalation_rules=["HIGH_RISK_DETECTED", "CONSENSUS_FAILED"],
            approval_requirements=["FUND_TRANSFER_>_10000", "PORTFOLIO_REBALANCE"],
            policies=["SYS_SEC_01", "SYS_GOV_01"],
            description="The Executive Cognitive Supervisor orchestrates all other agents and resolves conflicts."
        ))

        self.register(AgentDefinition(
            id="agent_budget_01",
            role=AgentRole.BUDGET,
            capabilities=["expense_categorization", "anomaly_detection", "budget_adjustment"],
            allowed_tools=["query_ledger", "update_budget_envelope", "send_notification"],
            memory_scope=MemoryScope.MISSION,
            escalation_rules=["BUDGET_EXCEEDED_BY_20_PERCENT"],
            approval_requirements=["CREATE_NEW_BUDGET_CATEGORY"],
            policies=["FIN_BUD_01"],
            description="Manages day-to-day budget tracking and categorization."
        ))

        self.register(AgentDefinition(
            id="agent_risk_01",
            role=AgentRole.RISK,
            capabilities=["portfolio_volatility_analysis", "exposure_calculation", "stress_testing"],
            allowed_tools=["query_market_data", "query_portfolio", "run_monte_carlo"],
            memory_scope=MemoryScope.LONG_TERM,
            escalation_rules=["VAR_EXCEEDED_THRESHOLD", "MARGIN_CALL_RISK"],
            approval_requirements=["LIQUIDATE_ASSETS"],
            policies=["FIN_RSK_01", "FIN_RSK_02"],
            description="Continuously monitors overall financial risk and exposure."
        ))

        # We can register the remaining 15 agents similarly.
        # This acts as the canonical definitions.

    def register(self, agent: AgentDefinition):
        self._agents[agent.role] = agent

    def get_agent(self, role: AgentRole) -> Optional[AgentDefinition]:
        return self._agents.get(role)

    def get_all_agents(self) -> List[AgentDefinition]:
        return list(self._agents.values())
