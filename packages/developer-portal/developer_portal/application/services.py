from typing import Dict, Any, List
import yaml

class CatalogService:
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}
        
    def register_package(self, manifest: Dict[str, Any]):
        package_name = manifest.get("name")
        if not package_name:
            raise ValueError("Manifest must contain 'name'")
        self.registry[package_name] = manifest
        
    def get_catalog(self) -> List[Dict[str, Any]]:
        return list(self.registry.values())
        
    def get_package(self, package_name: str) -> Dict[str, Any]:
        return self.registry.get(package_name)

class DiscoveryService:
    def __init__(self, catalog: CatalogService):
        self.catalog = catalog
        
    def discover_from_yaml(self, yaml_content: str):
        """
        Parses a MANIFEST.yaml file emitted from a CI/CD event and registers it.
        """
        try:
            manifest = yaml.safe_load(yaml_content)
            self.catalog.register_package(manifest)
            return manifest.get("name")
        except Exception as e:
            raise ValueError(f"Invalid MANIFEST format: {e}")
