from typing import Dict, Any, List, Optional


class PlatformRegistryService:
    def __init__(self):
        # Maps capability (e.g. EXTRACT_RECEIPT) to a list of services providing it
        self.capabilities: Dict[str, List[Dict[str, Any]]] = {}

    def register_service(
        self, service_name: str, endpoint: str, provided_capabilities: List[str]
    ):
        service_record = {
            "name": service_name,
            "endpoint": endpoint,
            "status": "healthy",
        }
        for cap in provided_capabilities:
            if cap not in self.capabilities:
                self.capabilities[cap] = []
            self.capabilities[cap].append(service_record)

    def discover_capability(self, capability: str) -> Optional[Dict[str, Any]]:
        # Returns the first healthy service providing the capability
        services = self.capabilities.get(capability, [])
        for svc in services:
            if svc["status"] == "healthy":
                return svc
        return None


class ConfigurationService:
    def __init__(self):
        self.flags: Dict[str, bool] = {"use_new_ocr": False, "enable_ai_agent": True}
        self.configs: Dict[str, str] = {"max_tokens_per_user": "5000"}

    def get_flag(self, flag_name: str) -> bool:
        return self.flags.get(flag_name, False)

    def get_config(self, config_key: str) -> str:
        return self.configs.get(config_key, "")

    def update_flag(self, flag_name: str, value: bool):
        # In a real system, this would emit a Redis Pub/Sub event to flush local caches in Data Plane
        self.flags[flag_name] = value
