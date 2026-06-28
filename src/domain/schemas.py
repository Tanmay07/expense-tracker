from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from src.domain.enums import AccountType, AccountStatus, EntryType

class AccountCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    account_type: AccountType
    currency_code: str = Field(..., min_length=3, max_length=3)
    institution_id: Optional[str] = None
    opening_balance: float = 0.0
    is_primary: bool = False
    user_id: str

class AccountResponse(AccountCreate):
    id: str
    status: AccountStatus
    current_balance: float
    available_balance: float
    is_hidden: bool
    created_at: datetime
    updated_at: datetime
    version: int
    
    class Config:
        from_attributes = True

class LedgerEntryCreate(BaseModel):
    account_id: str
    entry_type: EntryType
    amount: float = Field(..., gt=0)
    reference_id: str
    description: Optional[str] = None

class LedgerEntryResponse(LedgerEntryCreate):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class AccountStatusUpdate(BaseModel):
    status: AccountStatus
    user_id: str # To verify ownership

class TransactionCreate(BaseModel):
    account_id: str
    amount: float = Field(..., gt=0)
    transaction_type: str # EXPENSE, INCOME, TRANSFER
    status: str = "CLEARED"
    merchant: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None
    transaction_date: Optional[datetime] = None
    reference_id: Optional[str] = None
    transfer_reference_id: Optional[str] = None
    source: str = "MANUAL"
    user_id: str

class TransactionResponse(TransactionCreate):
    id: str
    created_at: datetime
    updated_at: datetime
    version: int
    is_deleted: bool
    merchant_id: Optional[str] = None
    category_id: Optional[str] = None
    
    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryResponse(CategoryCreate):
    id: str
    category_type: str
    
    class Config:
        from_attributes = True

class MerchantCreate(BaseModel):
    name: str
    default_category_id: Optional[str] = None
    logo_url: Optional[str] = None

class MerchantResponse(MerchantCreate):
    id: str
    is_verified: bool
    
    class Config:
        from_attributes = True

class RuleCreate(BaseModel):
    rule_type: str
    condition_field: str
    condition_operator: str
    condition_value: str
    action_type: str
    action_value: str
    priority: int = 100

class RuleResponse(RuleCreate):
    id: str
    
    class Config:
        from_attributes = True

class NetWorthResponse(BaseModel):
    total_assets: float
    total_liabilities: float
    net_worth: float
    currency_code: str = "USD"

class DuplicateResponse(BaseModel):
    id: str
    transaction_id: str
    potential_duplicate_of_id: str
    similarity_score: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class SnapshotResponse(BaseModel):
    id: str
    account_id: str
    snapshot_date: datetime
    period: str
    closing_balance: float
    total_in: float
    total_out: float
    
    class Config:
        from_attributes = True
