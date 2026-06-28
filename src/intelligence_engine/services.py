from typing import Dict, Any, List

class FeatureStoreService:
    """
    Mock implementation of a Feature Store.
    In production, this queries Redis for pre-aggregated features 
    (e.g. daily_spend_velocity, frequent_merchants).
    """
    def get_user_features(self, user_id: str) -> Dict[str, Any]:
        # Return mock aggregated features
        return {
            "avg_transaction_size": 45.50,
            "weekend_spend_ratio": 0.65,
            "frequent_merchants": ["Starbucks", "Amazon", "Uber"]
        }

class CategorizationService:
    """
    Implements a strict Hybrid AI fallback pipeline for Categorization.
    User Rules -> Graph -> ML -> LLM
    """
    def categorize_transaction(self, merchant_name: str, amount: float) -> Dict[str, Any]:
        # 1. User Rules (Mock)
        if merchant_name == "Landlord LLC":
            return {"category": "Housing", "confidence": 1.0, "source": "USER_RULE"}
            
        # 2. ML Classification (Mock XGBoost output)
        ml_confidence = 0.95 if merchant_name == "Amazon" else 0.60
        
        if ml_confidence >= 0.75:
            return {"category": "Shopping", "confidence": ml_confidence, "source": "ML_CLASSIFIER"}
            
        # 3. LLM Fallback
        # In production this calls the Core AI Platform ModelRouter
        return {"category": "Entertainment", "confidence": 0.85, "source": "LLM_SEMANTIC_FALLBACK"}

class AnomalyDetectionService:
    """
    Identifies unusual transactions based on isolation forest 
    outlier scoring against the user's historical feature vector.
    """
    def __init__(self, feature_store: FeatureStoreService):
        self.feature_store = feature_store
        
    def score_transaction(self, user_id: str, amount: float) -> Dict[str, Any]:
        features = self.feature_store.get_user_features(user_id)
        avg_spend = features["avg_transaction_size"]
        
        # Simple mock logic: if amount is 10x the average, flag it
        is_anomaly = amount > (avg_spend * 10)
        
        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": 0.99 if is_anomaly else 0.10,
            "reason": "Amount exceeds historical variance threshold" if is_anomaly else "Normal"
        }
