from data_intelligence.domain.events import FinancialEvent
from typing import List


class CategorizationService:
    def enrich(self, event: FinancialEvent) -> FinancialEvent:
        # Mocking an AI / Rule Engine classification
        if "Uber" in event.merchant_raw:
            event.merchant_normalized = "Uber"
            event.category = "Transportation"
            event.ai_confidence = 0.95
        elif "STARBUCKS" in event.merchant_raw:
            event.merchant_normalized = "Starbucks"
            event.category = "Food & Drink"
            event.ai_confidence = 0.98
        return event


class DuplicateService:
    def __init__(self):
        self.seen_hashes = set()

    def check_duplicate(self, event: FinancialEvent) -> FinancialEvent:
        # Simple fuzzy hash for demo: date + amount + merchant
        sig = f"{event.transaction_date.date()}_{event.amount}_{event.merchant_raw}"
        if sig in self.seen_hashes:
            event.status = "DUPLICATE"
        else:
            self.seen_hashes.add(sig)
        return event


class PipelineService:
    def __init__(self, cat_svc: CategorizationService, dup_svc: DuplicateService):
        self.cat_svc = cat_svc
        self.dup_svc = dup_svc
        # In memory staging DB for parsed events
        self.staged_events: List[FinancialEvent] = []

    def process(self, raw_events: List[FinancialEvent]):
        for event in raw_events:
            # 1. Categorize & Normalize Merchant
            event = self.cat_svc.enrich(event)

            # 2. Check Duplicates
            event = self.dup_svc.check_duplicate(event)

            # 3. Data Quality Engine / Auto-Verify
            if event.status != "DUPLICATE":
                if event.ai_confidence > 0.90:
                    event.status = "VERIFIED"
                else:
                    event.status = "PENDING_REVIEW"

            self.staged_events.append(event)

    def get_pending_reviews(self, user_id: str) -> List[FinancialEvent]:
        return [
            e
            for e in self.staged_events
            if e.user_id == user_id and e.status == "PENDING_REVIEW"
        ]
