from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from src.infrastructure.models import Account, LedgerEntry, AccountAudit
from src.domain.schemas import AccountCreate, LedgerEntryCreate

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, account_data: AccountCreate) -> Account:
        db_account = Account(
            name=account_data.name,
            account_type=account_data.account_type,
            currency_code=account_data.currency_code,
            institution_id=account_data.institution_id,
            opening_balance=account_data.opening_balance,
            current_balance=0.0,
            available_balance=0.0,
            is_primary=account_data.is_primary,
            user_id=account_data.user_id
        )
        self.db.add(db_account)
        self.db.commit()
        self.db.refresh(db_account)
        return db_account
        
    def get_by_id(self, account_id: str) -> Optional[Account]:
        return self.db.query(Account).filter(Account.id == account_id).first()
        
    def list_for_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Account]:
        return self.db.query(Account).filter(Account.user_id == user_id).offset(skip).limit(limit).all()

    def update_status(self, account: Account, status: str) -> Account:
        account.status = status
        self.db.commit()
        self.db.refresh(account)
        return account
        
    def update_balance(self, account_id: str, new_current: float, new_available: float):
        account = self.get_by_id(account_id)
        if account:
            account.current_balance = new_current
            account.available_balance = new_available
            account.version += 1
            self.db.commit()

class LedgerRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def add_entry(self, entry_data: LedgerEntryCreate) -> LedgerEntry:
        db_entry = LedgerEntry(
            account_id=entry_data.account_id,
            entry_type=entry_data.entry_type,
            amount=entry_data.amount,
            reference_id=entry_data.reference_id,
            description=entry_data.description
        )
        self.db.add(db_entry)
        self.db.commit()
        self.db.refresh(db_entry)
        return db_entry
        
    def get_entries_for_account(self, account_id: str, skip: int = 0, limit: int = 100) -> List[LedgerEntry]:
        return self.db.query(LedgerEntry).filter(LedgerEntry.account_id == account_id).order_by(LedgerEntry.created_at.desc()).offset(skip).limit(limit).all()

class AuditRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def log_action(self, account_id: str, action: str, user_id: str, old_values: dict = None, new_values: dict = None):
        audit = AccountAudit(
            account_id=account_id,
            action=action,
            user_id=user_id,
            old_values=old_values,
            new_values=new_values
        )
        self.db.add(audit)
        self.db.commit()

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, data: 'TransactionCreate') -> 'Transaction':
        from src.infrastructure.models import Transaction
        import uuid
        
        db_txn = Transaction(
            id=str(uuid.uuid4()),
            user_id=data.user_id,
            account_id=data.account_id,
            amount=data.amount,
            transaction_type=data.transaction_type,
            status=data.status,
            merchant=data.merchant,
            category=data.category,
            notes=data.notes,
            transaction_date=data.transaction_date,
            reference_id=data.reference_id,
            transfer_reference_id=data.transfer_reference_id,
            source=data.source
        )
        self.db.add(db_txn)
        self.db.commit()
        self.db.refresh(db_txn)
        return db_txn
        
    def get_by_id(self, txn_id: str) -> Optional['Transaction']:
        from src.infrastructure.models import Transaction
        return self.db.query(Transaction).filter(Transaction.id == txn_id, Transaction.is_deleted == False).first()
        
    def update_status(self, txn: 'Transaction', status: str) -> 'Transaction':
        txn.status = status
        txn.version += 1
        self.db.commit()
        self.db.refresh(txn)
        return txn
        
    def soft_delete(self, txn: 'Transaction') -> 'Transaction':
        txn.is_deleted = True
        txn.version += 1
        self.db.commit()
        return txn
        
    def list_for_user(self, user_id: str) -> list['Transaction']:
        from src.infrastructure.models import Transaction
        return self.db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.is_deleted == False).all()

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, data: 'CategoryCreate', user_id: str = None) -> 'Category':
        from src.infrastructure.models import Category
        db_cat = Category(name=data.name, parent_id=data.parent_id, icon=data.icon, color=data.color, user_id=user_id)
        if user_id:
            db_cat.category_type = "CUSTOM"
        self.db.add(db_cat)
        self.db.commit()
        self.db.refresh(db_cat)
        return db_cat
        
    def get_by_name(self, name: str) -> Optional['Category']:
        from src.infrastructure.models import Category
        return self.db.query(Category).filter(Category.name.ilike(name)).first()

class MerchantRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, data: 'MerchantCreate') -> 'Merchant':
        from src.infrastructure.models import Merchant
        db_merch = Merchant(name=data.name, default_category_id=data.default_category_id, logo_url=data.logo_url)
        self.db.add(db_merch)
        self.db.commit()
        self.db.refresh(db_merch)
        return db_merch
        
    def get_by_name(self, name: str) -> Optional['Merchant']:
        from src.infrastructure.models import Merchant
        return self.db.query(Merchant).filter(Merchant.name.ilike(name)).first()
        
    def get_by_alias(self, alias_name: str) -> Optional['Merchant']:
        from src.infrastructure.models import Merchant, MerchantAlias
        alias = self.db.query(MerchantAlias).filter(MerchantAlias.alias.ilike(alias_name)).first()
        if alias:
            return self.db.query(Merchant).filter(Merchant.id == alias.merchant_id).first()
        return None

class RuleRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_rules_for_user(self, user_id: str) -> List['ClassificationRule']:
        from src.infrastructure.models import ClassificationRule
        return self.db.query(ClassificationRule).filter(
            or_(ClassificationRule.user_id == user_id, ClassificationRule.user_id == None)
        ).order_by(ClassificationRule.priority.desc()).all()

class DuplicateRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def add_duplicate_flag(self, txn_id: str, duplicate_of_id: str, score: float):
        from src.infrastructure.models import DuplicateTransaction
        dup = DuplicateTransaction(
            transaction_id=txn_id,
            potential_duplicate_of_id=duplicate_of_id,
            similarity_score=score
        )
        self.db.add(dup)
        self.db.commit()

class SnapshotRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_snapshot(self, account_id: str, date, period: str, closing: float, total_in: float, total_out: float):
        from src.infrastructure.models import BalanceSnapshot
        snap = BalanceSnapshot(
            account_id=account_id,
            snapshot_date=date,
            period=period,
            closing_balance=closing,
            total_in=total_in,
            total_out=total_out
        )
        self.db.add(snap)
        self.db.commit()
        self.db.refresh(snap)
        return snap
