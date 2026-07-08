from typing import List, Dict, Optional
from datetime import datetime
from wealth_foundation.domain.models import Household, FamilyMember, FXRate


class HouseholdService:
    def __init__(self):
        self.households: Dict[str, Household] = {}
        self.members: Dict[str, FamilyMember] = {}

    def create_household(self, name: str, base_currency: str = "USD") -> Household:
        h = Household(name=name, base_currency=base_currency)
        self.households[h.id] = h
        return h

    def add_member(
        self,
        household_id: str,
        name: str,
        role: str,
        ownership_percentage: float = 100.0,
        user_id: Optional[str] = None,
    ) -> FamilyMember:
        if household_id not in self.households:
            raise ValueError("Household not found")
        member = FamilyMember(
            household_id=household_id,
            user_id=user_id,
            name=name,
            role=role,
            ownership_percentage=ownership_percentage,
        )
        self.members[member.id] = member
        return member

    def get_household_members(self, household_id: str) -> List[FamilyMember]:
        return [m for m in self.members.values() if m.household_id == household_id]


class FXService:
    def __init__(self):
        self.rates: Dict[str, FXRate] = {}

    def _get_mock_rate(self, base: str, target: str) -> float:
        # Mock deterministic rates for testing
        mock_table = {
            "USD_EUR": 0.9,
            "EUR_USD": 1.11,
            "USD_INR": 83.0,
            "INR_USD": 0.012,
        }
        key = f"{base}_{target}"
        if key in mock_table:
            return mock_table[key]
        if base == target:
            return 1.0
        raise ValueError(f"Exchange rate not found for {base} to {target}")

    def fetch_live_rate(self, base_currency: str, target_currency: str) -> FXRate:
        rate_value = self._get_mock_rate(base_currency, target_currency)
        fx_rate = FXRate(
            base_currency=base_currency,
            target_currency=target_currency,
            rate=rate_value,
        )
        # Store latest rate
        key = f"{base_currency}_{target_currency}"
        self.rates[key] = fx_rate
        return fx_rate

    def convert(self, amount: float, base_currency: str, target_currency: str) -> float:
        rate = self.fetch_live_rate(base_currency, target_currency)
        return amount * rate.rate


from wealth_foundation.domain.models import CorporateAction, GoalFunding  # noqa: E402


class CorporateActionService:
    def __init__(self):
        self.actions: Dict[str, CorporateAction] = {}

    def announce_action(
        self,
        asset_symbol: str,
        action_type: str,
        ratio: Optional[float] = None,
        amount_per_share: Optional[float] = None,
    ) -> CorporateAction:
        ca = CorporateAction(
            asset_symbol=asset_symbol,
            action_type=action_type,
            ratio=ratio,
            amount_per_share=amount_per_share,
        )
        self.actions[ca.id] = ca
        return ca

    def get_pending_actions(self, asset_symbol: str) -> List[CorporateAction]:
        return [
            ca
            for ca in self.actions.values()
            if ca.asset_symbol == asset_symbol and ca.status == "PENDING"
        ]

    def mark_applied(self, action_id: str):
        if action_id in self.actions:
            self.actions[action_id].status = "APPLIED"


class GoalFundingService:
    def __init__(self):
        self.fundings: Dict[str, GoalFunding] = {}

    def link_asset_to_goal(
        self,
        goal_id: str,
        asset_id: str,
        allocation_percentage: float = 100.0,
        priority: int = 1,
    ) -> GoalFunding:
        gf = GoalFunding(
            goal_id=goal_id,
            asset_id=asset_id,
            allocation_percentage=allocation_percentage,
            priority=priority,
        )
        self.fundings[gf.id] = gf
        return gf

    def get_fundings_for_goal(self, goal_id: str) -> List[GoalFunding]:
        return [f for f in self.fundings.values() if f.goal_id == goal_id]


from wealth_foundation.domain.models import ProviderPlugin, WealthExplanation  # noqa: E402


class ProviderRegistryService:
    def __init__(self):
        self.providers: Dict[str, ProviderPlugin] = {}

    def register_provider(
        self,
        name: str,
        provider_type: str,
        priority: int = 1,
        capabilities: List[str] = [],
    ) -> ProviderPlugin:
        pp = ProviderPlugin(
            name=name,
            provider_type=provider_type,
            priority=priority,
            capabilities=capabilities,
        )
        self.providers[pp.id] = pp
        return pp

    def get_active_providers(self, provider_type: str) -> List[ProviderPlugin]:
        active = [
            p
            for p in self.providers.values()
            if p.provider_type == provider_type and p.is_active
        ]
        active.sort(key=lambda x: x.priority)
        return active


class ExplainabilityService:
    def __init__(self):
        self.explanations: Dict[str, WealthExplanation] = {}

    def log_explanation(
        self,
        recommendation_id: str,
        rule_applied: str,
        confidence_score: float,
        evidence: str,
    ) -> WealthExplanation:
        exp = WealthExplanation(
            recommendation_id=recommendation_id,
            rule_applied=rule_applied,
            confidence_score=confidence_score,
            evidence=evidence,
        )
        self.explanations[exp.id] = exp
        return exp

    def get_explanation(self, recommendation_id: str) -> Optional[WealthExplanation]:
        for exp in self.explanations.values():
            if exp.recommendation_id == recommendation_id:
                return exp
        return None


from wealth_foundation.domain.models import Custodian, Broker, AssetCustody  # noqa: E402


class CustodianService:
    def __init__(self):
        self.custodians: Dict[str, Custodian] = {}

    def register_custodian(
        self, name: str, custodian_type: str, capabilities: List[str] = []
    ) -> Custodian:
        c = Custodian(
            name=name, custodian_type=custodian_type, capabilities=capabilities
        )
        self.custodians[c.id] = c
        return c


class BrokerService:
    def __init__(self):
        self.brokers: Dict[str, Broker] = {}
        self.custody_records: Dict[str, AssetCustody] = {}

    def link_broker(self, custodian_id: str, name: str, auth_mechanism: str) -> Broker:
        b = Broker(custodian_id=custodian_id, name=name, auth_mechanism=auth_mechanism)
        self.brokers[b.id] = b
        return b

    def assign_custody(
        self, asset_id: str, broker_id: str, quantity: float
    ) -> AssetCustody:
        if broker_id not in self.brokers:
            raise ValueError("Broker not found")
        ac = AssetCustody(asset_id=asset_id, broker_id=broker_id, quantity=quantity)
        self.custody_records[ac.id] = ac
        return ac


from wealth_foundation.domain.models import TaxLot, WealthPolicy, PortfolioPolicy  # noqa: E402


class TaxLotService:
    def __init__(self):
        self.lots: Dict[str, TaxLot] = {}

    def generate_purchase_lot(
        self, asset_id: str, broker_id: str, quantity: float, unit_price: float
    ) -> TaxLot:
        lot = TaxLot(
            asset_id=asset_id,
            broker_id=broker_id,
            quantity=quantity,
            unit_price=unit_price,
        )
        self.lots[lot.id] = lot
        return lot

    def get_open_lots(self, asset_id: str, broker_id: str) -> List[TaxLot]:
        # Return sorted by purchase_date for FIFO
        lots = [
            lot
            for lot in self.lots.values()
            if lot.asset_id == asset_id
            and lot.broker_id == broker_id
            and lot.status == "OPEN"
        ]
        lots.sort(key=lambda x: x.purchase_date)
        return lots


class PolicyService:
    def __init__(self):
        self.wealth_policies: Dict[str, WealthPolicy] = {}
        self.portfolio_policies: Dict[str, PortfolioPolicy] = {}

    def create_wealth_policy(
        self, household_id: str, name: str, policy_type: str, parameters: dict
    ) -> WealthPolicy:
        p = WealthPolicy(
            household_id=household_id,
            name=name,
            policy_type=policy_type,
            parameters=parameters,
        )
        self.wealth_policies[p.id] = p
        return p

    def create_portfolio_policy(
        self, portfolio_id: str, name: str, policy_type: str, parameters: dict
    ) -> PortfolioPolicy:
        p = PortfolioPolicy(
            portfolio_id=portfolio_id,
            name=name,
            policy_type=policy_type,
            parameters=parameters,
        )
        self.portfolio_policies[p.id] = p
        return p


from wealth_foundation.domain.models import (  # noqa: E402
    HouseholdPermission,
    WealthSnapshot,
    ReplayState,
)


class PermissionService:
    def __init__(self):
        self.permissions: Dict[str, HouseholdPermission] = {}

    def grant_permission(
        self, household_id: str, user_id: str, role: str, granted_by: str
    ) -> HouseholdPermission:
        perm = HouseholdPermission(
            household_id=household_id, user_id=user_id, role=role, granted_by=granted_by
        )
        self.permissions[perm.id] = perm
        return perm

    def get_permissions(self, household_id: str) -> List[HouseholdPermission]:
        return [
            p
            for p in self.permissions.values()
            if p.household_id == household_id and p.is_active
        ]


class SnapshotService:
    def __init__(self):
        self.snapshots: Dict[str, WealthSnapshot] = {}

    def generate_snapshot(
        self,
        entity_id: str,
        entity_type: str,
        snapshot_date: datetime,
        net_worth: float,
        asset_allocation: dict,
    ) -> WealthSnapshot:
        snap = WealthSnapshot(
            entity_id=entity_id,
            entity_type=entity_type,
            snapshot_date=snapshot_date,
            net_worth=net_worth,
            asset_allocation=asset_allocation,
        )
        self.snapshots[snap.id] = snap
        return snap


class ReplayService:
    def __init__(self):
        self.replays: Dict[str, ReplayState] = {}

    def build_replay_state(
        self, entity_id: str, entity_type: str, target_date: datetime, state_data: dict
    ) -> ReplayState:
        rs = ReplayState(
            target_date=target_date,
            entity_id=entity_id,
            entity_type=entity_type,
            state_data=state_data,
        )
        self.replays[rs.id] = rs
        return rs
