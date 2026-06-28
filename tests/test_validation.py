from src.automation.validation import ValidationEngine, PositiveAmountSpecification, CurrencySupportedSpecification, Severity

def test_validation_engine_success():
    engine = ValidationEngine()
    engine.add_specification(PositiveAmountSpecification())
    engine.add_specification(CurrencySupportedSpecification(["USD", "EUR"]))
    
    context = {"amount": 50.0, "currency": "USD"}
    failures = engine.validate(context)
    
    assert len(failures) == 0

def test_validation_engine_failure_amount():
    engine = ValidationEngine()
    engine.add_specification(PositiveAmountSpecification())
    
    context = {"amount": -10.0, "currency": "USD"}
    failures = engine.validate(context)
    
    assert len(failures) == 1
    assert failures[0].error_code == "VAL_AMT_001"
    assert failures[0].severity == Severity.BLOCK

def test_validation_engine_and_specification():
    spec1 = PositiveAmountSpecification()
    spec2 = CurrencySupportedSpecification(["USD", "EUR"])
    combined_spec = spec1.and_spec(spec2)
    
    # Fails spec1
    res1 = combined_spec.is_satisfied_by({"amount": -5.0, "currency": "USD"})
    assert res1.is_valid == False
    assert res1.error_code == "VAL_AMT_001"
    
    # Fails spec2
    res2 = combined_spec.is_satisfied_by({"amount": 50.0, "currency": "GBP"})
    assert res2.is_valid == False
    assert res2.error_code == "VAL_CUR_001"
    
    # Passes both
    res3 = combined_spec.is_satisfied_by({"amount": 100.0, "currency": "EUR"})
    assert res3.is_valid == True
