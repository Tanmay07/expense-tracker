from financial_planning.domain.models import Budget, Goal
from typing import List, Dict, Optional, Any
import uuid
from datetime import datetime

class BudgetService:
    def __init__(self):
        # In-memory mock DB for Step 1 before full SQLAlchemy integration
        self.budgets: Dict[str, Budget] = {}
        
    def create_budget(self, user_id: str, name: str, amount: float, period: str, category_id: Optional[str] = None) -> Budget:
        budget = Budget(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=name,
            amount=amount,
            period=period,
            category_id=category_id,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() # Mocked
        )
        self.budgets[budget.id] = budget
        return budget
        
    def get_budgets(self, user_id: str) -> List[Budget]:
        return [b for b in self.budgets.values() if b.user_id == user_id]
        
    def record_spending(self, budget_id: str, amount: float) -> Budget:
        budget = self.budgets.get(budget_id)
        if not budget:
            raise ValueError("Budget not found")
            
        budget.spent_amount += amount
        if budget.spent_amount > budget.amount:
            budget.status = "EXCEEDED"
            
        return budget

class GoalService:
    def __init__(self):
        self.goals: Dict[str, Goal] = {}
        
    def create_goal(self, user_id: str, name: str, target_amount: float) -> Goal:
        goal = Goal(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=name,
            target_amount=target_amount
        )
        self.goals[goal.id] = goal
        return goal
        
    def get_goals(self, user_id: str) -> List[Goal]:
        return [g for g in self.goals.values() if g.user_id == user_id]
        
    def add_funds(self, goal_id: str, amount: float) -> Goal:
        goal = self.goals.get(goal_id)
        if not goal:
            raise ValueError("Goal not found")
            
        goal.current_amount += amount
        if goal.current_amount >= goal.target_amount:
            goal.status = "ACHIEVED"
            
        return goal

from financial_planning.domain.models import HealthScore, Recommendation, CashFlowForecast

class CashFlowService:
    def get_historical_cashflow(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        # Mocking generic cashflow logic that would read from Ledger DB
        return {
            "inflows": 5000.00,
            "outflows": 4200.00,
            "net_cashflow": 800.00,
            "period_days": days
        }

class ForecastService:
    def generate_forecast(self, user_id: str, days_ahead: int = 30) -> CashFlowForecast:
        # Simple mocked linear forecast
        # (Assuming $800 net positive per month)
        from datetime import timedelta
        proj_date = datetime.utcnow() + timedelta(days=days_ahead)
        return CashFlowForecast(
            user_id=user_id,
            projected_date=proj_date,
            projected_balance=1500.00, # Simulated
            confidence_interval=0.85
        )

class HealthService:
    def calculate_health_score(self, user_id: str) -> HealthScore:
        # Mocking a static calculation for Step 2
        return HealthScore(
            user_id=user_id,
            overall_score=75,
            savings_score=80,
            budget_score=60,
            debt_score=90
        )

class RecommendationService:
    def generate_recommendations(self, user_id: str, health: HealthScore) -> List[Recommendation]:
        recs = []
        if health.budget_score < 70:
            recs.append(Recommendation(
                user_id=user_id,
                title="Optimize Budget",
                description="Your budget score is low. Consider reducing non-essential spending.",
                action_type="REDUCE_SPENDING",
                priority="HIGH"
            ))
        if health.overall_score > 70:
            recs.append(Recommendation(
                user_id=user_id,
                title="Increase Savings Goal",
                description="Your financial health is solid. Consider increasing your Emergency Fund target.",
                action_type="INCREASE_SAVINGS",
                priority="MEDIUM"
            ))
        return recs

from financial_planning.domain.models import Subscription, Bill, RecurringTransaction, Reminder

class SubscriptionService:
    def __init__(self):
        self.subscriptions: Dict[str, Subscription] = {}
        
    def add_subscription(self, user_id: str, name: str, cost: float, billing_cycle: str, next_billing: datetime) -> Subscription:
        sub = Subscription(
            user_id=user_id,
            name=name,
            cost=cost,
            billing_cycle=billing_cycle,
            next_billing_date=next_billing
        )
        self.subscriptions[sub.id] = sub
        return sub

class BillService:
    def __init__(self):
        self.bills: Dict[str, Bill] = {}
        
    def add_bill(self, user_id: str, biller_name: str, amount: float, due_date: datetime) -> Bill:
        bill = Bill(
            user_id=user_id,
            biller_name=biller_name,
            amount=amount,
            due_date=due_date
        )
        self.bills[bill.id] = bill
        return bill
        
    def mark_paid(self, bill_id: str) -> Bill:
        bill = self.bills.get(bill_id)
        if bill:
            bill.status = "PAID"
        return bill

class RecurringService:
    def __init__(self):
        self.recurring: Dict[str, RecurringTransaction] = {}
        
    def setup_recurring(self, user_id: str, name: str, amount: float, tx_type: str, rrule: str) -> RecurringTransaction:
        rt = RecurringTransaction(
            user_id=user_id,
            name=name,
            amount=amount,
            transaction_type=tx_type,
            rrule=rrule
        )
        self.recurring[rt.id] = rt
        return rt

class ReminderService:
    def __init__(self):
        self.reminders: Dict[str, Reminder] = {}
        
    def create_reminder(self, user_id: str, title: str, message: str, trigger_date: datetime) -> Reminder:
        rem = Reminder(
            user_id=user_id,
            title=title,
            message=message,
            trigger_date=trigger_date
        )
        self.reminders[rem.id] = rem
        return rem
