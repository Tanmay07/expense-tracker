from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from src.infrastructure.database import Base
from src.domain.enums import AccountType, AccountStatus, EntryType

def generate_uuid():
    return str(uuid.uuid4())

def get_utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True)

class FinancialInstitution(Base):
    __tablename__ = "institutions"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, index=True)
    logo_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

class Currency(Base):
    __tablename__ = "currencies"
    code = Column(String(3), primary_key=True, index=True) # e.g. USD, INR
    name = Column(String)
    symbol = Column(String)

class Account(Base):
    __tablename__ = "accounts"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    institution_id = Column(String, ForeignKey("institutions.id"), nullable=True)
    
    name = Column(String, nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    currency_code = Column(String, ForeignKey("currencies.code"), nullable=False)
    
    is_primary = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
    
    # Balances
    opening_balance = Column(Float, default=0.0)
    current_balance = Column(Float, default=0.0)
    available_balance = Column(Float, default=0.0)
    
    # Metadata & Settings (JSON for flexibility)
    settings = Column(JSON, default={})
    metadata_info = Column(JSON, default={})
    
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    version = Column(Integer, default=1)

    ledgers = relationship("LedgerEntry", back_populates="account")

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"
    id = Column(String, primary_key=True, default=generate_uuid)
    account_id = Column(String, ForeignKey("accounts.id"), index=True, nullable=False)
    
    entry_type = Column(Enum(EntryType), nullable=False)
    amount = Column(Float, nullable=False) # Must always be positive
    
    reference_id = Column(String, index=True, nullable=False) # Maps to a Transaction ID
    description = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=get_utc_now)
    
    account = relationship("Account", back_populates="ledgers")

class AccountAudit(Base):
    __tablename__ = "account_audits"
    id = Column(String, primary_key=True, default=generate_uuid)
    account_id = Column(String, index=True, nullable=False)
    action = Column(String, nullable=False) # CREATE, UPDATE, FREEZE, CLOSE
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
    user_id = Column(String, nullable=False)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    account_id = Column(String, ForeignKey("accounts.id"), index=True, nullable=False)
    
    amount = Column(Float, nullable=False) # Always positive
    transaction_type = Column(String, nullable=False) # EXPENSE, INCOME, TRANSFER
    status = Column(String, default="CLEARED")
    
    merchant = Column(String, nullable=True) # Raw string from source
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=True)
    
    category = Column(String, nullable=True) # Legacy or raw category
    category_id = Column(String, ForeignKey("categories.id"), index=True, nullable=True)
    
    notes = Column(String, nullable=True)
    
    transaction_date = Column(DateTime, default=get_utc_now, index=True)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    
    reference_id = Column(String, unique=True, index=True, nullable=True)
    transfer_reference_id = Column(String, index=True, nullable=True)
    source = Column(String, default="MANUAL")
    
    version = Column(Integer, default=1)
    is_deleted = Column(Boolean, default=False)

class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, index=True, nullable=False)
    parent_id = Column(String, ForeignKey("categories.id"), nullable=True)
    user_id = Column(String, index=True, nullable=True) # Null = built-in
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)
    category_type = Column(String, default="BUILTIN")

class Merchant(Base):
    __tablename__ = "merchants"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, index=True, nullable=False)
    default_category_id = Column(String, ForeignKey("categories.id"), nullable=True)
    logo_url = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)

class MerchantAlias(Base):
    __tablename__ = "merchant_aliases"
    id = Column(String, primary_key=True, default=generate_uuid)
    merchant_id = Column(String, ForeignKey("merchants.id"), index=True, nullable=False)
    alias = Column(String, unique=True, index=True, nullable=False)

class ClassificationRule(Base):
    __tablename__ = "classification_rules"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, index=True, nullable=True) # Null = system rule
    rule_type = Column(String, nullable=False) # USER, MERCHANT, KEYWORD, DEFAULT
    priority = Column(Integer, default=100)
    
    condition_field = Column(String, nullable=False) # e.g. "merchant_name", "amount"
    condition_operator = Column(String, nullable=False) # EQUALS, CONTAINS
    condition_value = Column(String, nullable=False)
    
    action_type = Column(String, nullable=False) # SET_CATEGORY
    action_value = Column(String, nullable=False) # category_id

class BalanceSnapshot(Base):
    __tablename__ = "balance_snapshots"
    id = Column(String, primary_key=True, default=generate_uuid)
    account_id = Column(String, ForeignKey("accounts.id"), index=True, nullable=False)
    snapshot_date = Column(DateTime, nullable=False, index=True)
    period = Column(String, nullable=False) # DAILY, MONTHLY
    
    closing_balance = Column(Float, nullable=False)
    total_in = Column(Float, default=0.0)
    total_out = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=get_utc_now)

class DuplicateTransaction(Base):
    __tablename__ = "duplicate_transactions"
    id = Column(String, primary_key=True, default=generate_uuid)
    transaction_id = Column(String, ForeignKey("transactions.id"), index=True, nullable=False)
    potential_duplicate_of_id = Column(String, ForeignKey("transactions.id"), index=True, nullable=False)
    
    similarity_score = Column(Float, nullable=False)
    status = Column(String, default="PENDING") # PENDING, RESOLVED, IGNORED
    created_at = Column(DateTime, default=get_utc_now)

class SyncConflict(Base):
    __tablename__ = "sync_conflicts"
    id = Column(String, primary_key=True, default=generate_uuid)
    entity_type = Column(String, nullable=False) # ACCOUNT, TRANSACTION
    entity_id = Column(String, nullable=False, index=True)
    
    server_version = Column(Integer, nullable=False)
    client_version = Column(Integer, nullable=False)
    
    server_data = Column(JSON, nullable=False)
    client_data = Column(JSON, nullable=False)
    
    status = Column(String, default="UNRESOLVED")
    created_at = Column(DateTime, default=get_utc_now)

class RawDataImport(Base):
    __tablename__ = "raw_data_imports"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, index=True, nullable=False)
    source = Column(String, nullable=False) # CSV, PDF, SMS
    
    storage_path = Column(String, nullable=False) # S3 or local path
    original_filename = Column(String, nullable=True)
    file_hash = Column(String, nullable=True, index=True)
    
    status = Column(String, default="PENDING")
    records_processed = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

