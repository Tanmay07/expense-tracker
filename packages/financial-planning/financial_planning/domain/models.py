from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Budget(BaseModel):
    """
    A planned limit on spending for a given category/merchant over a time period.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    amount: float
    currency_code: str = "USD"
    period: str # MONTHLY, WEEKLY, YEARLY
    
    # Target constraints
    category_id: Optional[str] = None
    merchant_id: Optional[str] = None
    
    # Tracked Progress
    spent_amount: float = 0.0
    
    start_date: datetime
    end_date: datetime
    
    status: str = "ACTIVE" # ACTIVE, EXCEEDED, ARCHIVED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class Goal(BaseModel):
    """
    A savings objective with a target amount.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    target_amount: float
    current_amount: float = 0.0
    currency_code: str = "USD"
    
    target_date: Optional[datetime] = None
    priority: int = 1 # 1 (High) to 5 (Low)
    
    # Linked account where funds are held (optional)
    funding_account_id: Optional[str] = None
    
    status: str = "IN_PROGRESS" # IN_PROGRESS, ACHIEVED, PAUSED
    created_at: datetime = Field(default_factory=datetime.utcnow)

class HealthScore(BaseModel):
    user_id: str
    overall_score: int # 0 to 100
    savings_score: int
    budget_score: int
    debt_score: int
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    
class Recommendation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    description: str
    action_type: str # REDUCE_SPENDING, INCREASE_SAVINGS, PAY_DEBT
    priority: str # HIGH, MEDIUM, LOW
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class CashFlowForecast(BaseModel):
    user_id: str
    projected_date: datetime
    projected_balance: float
    confidence_interval: float # e.g. 0.95
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Subscription(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str # Netflix, Spotify, Gym
    cost: float
    currency_code: str = "USD"
    billing_cycle: str # MONTHLY, YEARLY
    next_billing_date: datetime
    status: str = "ACTIVE" # ACTIVE, CANCELLED
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Bill(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    biller_name: str # Electric Co, Internet Provider
    amount: float
    due_date: datetime
    status: str = "UNPAID" # UNPAID, PAID, OVERDUE
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RecurringTransaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str # Salary, Rent
    amount: float
    transaction_type: str # INCOME, EXPENSE
    rrule: str # RRULE scheduling (e.g. FREQ=MONTHLY;BYMONTHDAY=1)
    status: str = "ACTIVE" # ACTIVE, PAUSED
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Reminder(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    message: str
    trigger_date: datetime
    is_sent: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
