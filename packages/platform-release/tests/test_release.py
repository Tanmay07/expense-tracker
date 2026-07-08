def test_capture_baseline(client):
    response = client.post("/api/v1/platform/baseline?version=1.0.0")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "captured"
    assert "baseline_id" in data


def test_freeze_contracts(client):
    response = client.post("/api/v1/platform/contracts/freeze?version=1.0.0")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "frozen"
    assert "contract_matrix_id" in data


def test_freeze_documentation(client):
    response = client.post("/api/v1/platform/documentation/freeze?version=1.0.0")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "frozen"
    assert "documentation_index_id" in data


def test_certify_release(client):
    response = client.post("/api/v1/platform/certification?version=1.0.0")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "certified"
    assert "certification_id" in data


def test_generate_and_fetch_release(client):
    # Setup dependencies
    baseline_id = client.post("/api/v1/platform/baseline?version=1.0.0").json()[
        "baseline_id"
    ]
    cert_id = client.post("/api/v1/platform/certification?version=1.0.0").json()[
        "certification_id"
    ]
    contract_id = client.post("/api/v1/platform/contracts/freeze?version=1.0.0").json()[
        "contract_matrix_id"
    ]
    doc_id = client.post("/api/v1/platform/documentation/freeze?version=1.0.0").json()[
        "documentation_index_id"
    ]

    # Generate release
    response = client.post(
        "/api/v1/platform/release",
        params={
            "version": "1.0.0",
            "certification_id": cert_id,
            "baseline_id": baseline_id,
            "contract_matrix_id": contract_id,
            "doc_index_id": doc_id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "published"

    # Fetch release
    fetch_res = client.get("/api/v1/platform/version/1.0.0")
    assert fetch_res.status_code == 200
    assert fetch_res.json()["version"] == "1.0.0"

    # Check readiness
    ready_res = client.get("/api/v1/platform/readiness/1.0.0")
    assert ready_res.status_code == 200
    assert ready_res.json()["ready"]


def test_governance_lifecycle(client):
    response = client.get("/api/v1/platform/governance/lifecycle")
    assert response.status_code == 200
    assert response.json()["status"] == "valid"
