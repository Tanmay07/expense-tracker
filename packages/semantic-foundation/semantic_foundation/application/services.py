from typing import Dict, Any, List

class GlossaryService:
    def __init__(self):
        # Term ID -> Definition (The Ubiquitous Language)
        self.terms: Dict[str, Dict[str, Any]] = {}
        
    def register_term(self, term_id: str, business_name: str, definition: str, domain: str):
        self.terms[term_id] = {
            "business_name": business_name,
            "definition": definition,
            "domain": domain,
            "status": "APPROVED"
        }
        return term_id

    def get_term(self, term_id: str) -> Dict[str, Any]:
        return self.terms.get(term_id)

class MetadataService:
    def __init__(self):
        # Concept ID -> Metadata properties
        self.metadata_store: Dict[str, Dict[str, Any]] = {}
        
    def tag_concept(self, concept_id: str, tags: List[str], documentation_url: str):
        if concept_id not in self.metadata_store:
            self.metadata_store[concept_id] = {"tags": [], "documentation": ""}
            
        self.metadata_store[concept_id]["tags"].extend(tags)
        self.metadata_store[concept_id]["documentation"] = documentation_url

    def get_metadata(self, concept_id: str) -> Dict[str, Any]:
        return self.metadata_store.get(concept_id, {})
