from abc import ABC, abstractmethod
from typing import Any, List, Dict
from enum import Enum
from pydantic import BaseModel

class Severity(str, Enum):
    INFO = "INFO"
    WARN = "WARN"
    BLOCK = "BLOCK"

class ValidationResult(BaseModel):
    is_valid: bool
    severity: Severity
    error_code: str
    message: str

class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, context: Dict[str, Any]) -> ValidationResult:
        pass
        
    def and_spec(self, other: 'Specification') -> 'Specification':
        return AndSpecification(self, other)

class AndSpecification(Specification):
    def __init__(self, spec1: Specification, spec2: Specification):
        self.spec1 = spec1
        self.spec2 = spec2
        
    def is_satisfied_by(self, context: Dict[str, Any]) -> ValidationResult:
        res1 = self.spec1.is_satisfied_by(context)
        if not res1.is_valid:
            return res1
        return self.spec2.is_satisfied_by(context)

class PositiveAmountSpecification(Specification):
    def is_satisfied_by(self, context: Dict[str, Any]) -> ValidationResult:
        amount = context.get("amount", 0.0)
        if amount <= 0:
            return ValidationResult(is_valid=False, severity=Severity.BLOCK, error_code="VAL_AMT_001", message="Amount must be positive.")
        return ValidationResult(is_valid=True, severity=Severity.INFO, error_code="", message="")

class CurrencySupportedSpecification(Specification):
    def __init__(self, supported_currencies: List[str]):
        self.supported_currencies = supported_currencies
        
    def is_satisfied_by(self, context: Dict[str, Any]) -> ValidationResult:
        curr = context.get("currency", "USD")
        if curr not in self.supported_currencies:
            return ValidationResult(is_valid=False, severity=Severity.BLOCK, error_code="VAL_CUR_001", message=f"Currency {curr} not supported.")
        return ValidationResult(is_valid=True, severity=Severity.INFO, error_code="", message="")

class ValidationEngine:
    def __init__(self):
        self.specs: List[Specification] = []
        
    def add_specification(self, spec: Specification):
        self.specs.append(spec)
        
    def validate(self, context: Dict[str, Any]) -> List[ValidationResult]:
        failures = []
        for spec in self.specs:
            res = spec.is_satisfied_by(context)
            if not res.is_valid:
                failures.append(res)
        return failures
