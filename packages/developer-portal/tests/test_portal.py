import pytest
import urllib.parse
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.mark.skip(reason="Pending package implementation")
def test_portal_discovery():
    manifest = """
    name: platform-sdk
    description: Core Platform SDK
    maturity: Enterprise
    owner: platform-team
    """
    encoded_manifest = urllib.parse.quote(manifest)
    
    # Trigger CI/CD Webhook to discover the package
    res1 = client.post(f"/api/v1/portal/discover?manifest_yaml={encoded_manifest}")
    assert res1.status_code == 200
    assert res1.json()["status"] == "registered"
    assert res1.json()["package"] == "platform-sdk"
    
    # Query the Developer Portal Catalog
    res2 = client.get("/api/v1/portal/catalog")
    assert res2.status_code == 200
    catalog = res2.json()["packages"]
    assert len(catalog) >= 1
    
    # Verify Metadata Indexed
    pkg = next(p for p in catalog if p["name"] == "platform-sdk")
    assert pkg["maturity"] == "Enterprise"
    assert pkg["owner"] == "platform-team"
