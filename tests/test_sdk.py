import pytest
from src.sdk.common.exceptions import PlatformError, ValidationException
from src.sdk.common.events import CloudEvent

def test_platform_error_hierarchy():
    err = ValidationException("Invalid email format")
    assert isinstance(err, PlatformError)
    assert err.code == "ERR_VALIDATION"
    assert err.is_retryable is False

def test_cloudevent_schema():
    event = CloudEvent(
        source="/test/service",
        type="test.event.emitted",
        data={"user": "test_123"},
        tenant_id="tenant_x"
    )
    
    assert event.specversion == "1.0"
    assert event.id is not None
    assert event.datacontenttype == "application/json"
    assert event.data["user"] == "test_123"
    assert event.tenant_id == "tenant_x"
