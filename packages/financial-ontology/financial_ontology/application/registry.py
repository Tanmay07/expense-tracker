import json
import os
from typing import Dict, Any


class OntologyRegistryService:
    def __init__(self):
        # Concept ID -> Canonical Definition
        self.concepts: Dict[str, Dict[str, Any]] = {}

    def load_from_code(self, file_path: str):
        """Loads Ontology-as-Code definitions from a JSON/YAML file."""
        if not os.path.exists(file_path):
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        for concept in data.get("concepts", []):
            self.concepts[concept["id"]] = concept

    def get_concept(self, concept_id: str) -> Dict[str, Any]:
        return self.concepts.get(concept_id)

    def search_concept_by_alias(self, alias: str) -> Dict[str, Any]:
        alias_lower = alias.lower()
        for concept in self.concepts.values():
            aliases = [a.lower() for a in concept.get("aliases", [])]
            if alias_lower in aliases or alias_lower == concept["name"].lower():
                return concept
        return None
