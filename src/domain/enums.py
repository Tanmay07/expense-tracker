from enum import Enum

class AccountType(str, Enum):
    BANK = "BANK"
    CREDIT_CARD = "CREDIT_CARD"
    CASH_WALLET = "CASH_WALLET"
    UPI = "UPI"
    DIGITAL_WALLET = "DIGITAL_WALLET"
    LOAN = "LOAN"
    INVESTMENT = "INVESTMENT"

class AccountStatus(str, Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"

class EntryType(str, Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class TransactionType(str, Enum):
    EXPENSE = "EXPENSE"
    INCOME = "INCOME"
    TRANSFER = "TRANSFER"
    ADJUSTMENT = "ADJUSTMENT"
    REFUND = "REFUND"
    CASHBACK = "CASHBACK"

class TransactionStatus(str, Enum):
    PENDING = "PENDING"
    CLEARED = "CLEARED"
    RECONCILED = "RECONCILED"
    CANCELLED = "CANCELLED"

class TransactionSource(str, Enum):
    MANUAL = "MANUAL"
    SMS = "SMS"
    EMAIL = "EMAIL"
    OCR = "OCR"
    API = "API"

class CategoryType(str, Enum):
    BUILTIN = "BUILTIN"
    CUSTOM = "CUSTOM"

class RuleType(str, Enum):
    USER = "USER"
    MERCHANT = "MERCHANT"
    KEYWORD = "KEYWORD"
    DEFAULT = "DEFAULT"

class RuleCondition(str, Enum):
    EQUALS = "EQUALS"
    CONTAINS = "CONTAINS"
    STARTS_WITH = "STARTS_WITH"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"

class RuleAction(str, Enum):
    SET_CATEGORY = "SET_CATEGORY"
    SET_TAG = "SET_TAG"
    SET_MERCHANT = "SET_MERCHANT"

class ReconciliationStatus(str, Enum):
    PENDING = "PENDING"
    RECONCILED = "RECONCILED"
    CONFLICT = "CONFLICT"

class SnapshotPeriod(str, Enum):
    DAILY = "DAILY"
    MONTHLY = "MONTHLY"

class IngestionStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    NEEDS_REVIEW = "NEEDS_REVIEW"

class ImportSource(str, Enum):
    CSV = "CSV"
    PDF = "PDF"
    SMS = "SMS"
    EMAIL = "EMAIL"
    API = "API"
