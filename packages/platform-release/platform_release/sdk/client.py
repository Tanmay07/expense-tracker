import requests

class PlatformManagementSDK:
    def __init__(self, base_url: str = "http://platform-release-api:8000"):
        self.base_url = base_url

    def get_platform_version(self, version: str) -> dict:
        response = requests.get(f"{self.base_url}/api/v1/platform/version/{version}")
        response.raise_for_status()
        return response.json()

    def check_readiness(self, version: str) -> dict:
        response = requests.get(f"{self.base_url}/api/v1/platform/readiness/{version}")
        response.raise_for_status()
        return response.json()

    def certify_release(self, version: str) -> dict:
        response = requests.post(f"{self.base_url}/api/v1/platform/certification", params={"version": version})
        response.raise_for_status()
        return response.json()

    def capture_baseline(self, version: str) -> dict:
        response = requests.post(f"{self.base_url}/api/v1/platform/baseline", params={"version": version})
        response.raise_for_status()
        return response.json()

    def freeze_contracts(self, version: str) -> dict:
        response = requests.post(f"{self.base_url}/api/v1/platform/contracts/freeze", params={"version": version})
        response.raise_for_status()
        return response.json()

    def freeze_documentation(self, version: str) -> dict:
        response = requests.post(f"{self.base_url}/api/v1/platform/documentation/freeze", params={"version": version})
        response.raise_for_status()
        return response.json()

    def generate_release(self, version: str, cert_id: str, base_id: str, contract_id: str, doc_id: str) -> dict:
        response = requests.post(
            f"{self.base_url}/api/v1/platform/release",
            params={
                "version": version,
                "certification_id": cert_id,
                "baseline_id": base_id,
                "contract_matrix_id": contract_id,
                "doc_index_id": doc_id
            }
        )
        response.raise_for_status()
        return response.json()

    def get_lifecycle(self) -> dict:
        response = requests.get(f"{self.base_url}/api/v1/platform/governance/lifecycle")
        response.raise_for_status()
        return response.json()
