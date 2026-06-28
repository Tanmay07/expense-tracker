import json
import base64
import hmac
import hashlib
import time
from typing import Dict, Any, Optional

SECRET_KEY = "wave1_production_super_secret_key"

class AuthService:
    def __init__(self):
        # User ID -> { "email": str, "password_hash": str, "preferences": dict }
        self.users: Dict[str, Dict[str, Any]] = {}
        
    def _hash_password(self, password: str) -> str:
        # In a real system, use passlib + bcrypt.
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, email: str, password: str) -> str:
        import uuid
        user_id = str(uuid.uuid4())
        self.users[user_id] = {
            "email": email,
            "password_hash": self._hash_password(password),
            "preferences": {
                "currency": "USD",
                "timezone": "UTC",
                "language": "en"
            }
        }
        return user_id

    def authenticate(self, email: str, password: str) -> Optional[str]:
        pwd_hash = self._hash_password(password)
        for uid, data in self.users.items():
            if data["email"] == email and data["password_hash"] == pwd_hash:
                return uid
        return None

    def create_jwt(self, user_id: str) -> str:
        header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
        payload = base64.urlsafe_b64encode(json.dumps({
            "sub": user_id,
            "exp": int(time.time()) + 3600  # 1 hour expiration
        }).encode()).decode().rstrip("=")
        
        signature = base64.urlsafe_b64encode(
            hmac.new(SECRET_KEY.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
        ).decode().rstrip("=")
        
        return f"{header}.{payload}.{signature}"
        
    def verify_jwt(self, token: str) -> Optional[str]:
        try:
            header, payload, signature = token.split(".")
            expected_sig = base64.urlsafe_b64encode(
                hmac.new(SECRET_KEY.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
            ).decode().rstrip("=")
            
            if not hmac.compare_digest(signature, expected_sig):
                return None
                
            decoded_payload = json.loads(base64.urlsafe_b64decode(payload + "===").decode())
            if decoded_payload["exp"] < time.time():
                return None
                
            return decoded_payload["sub"]
        except Exception:
            return None

    def update_preferences(self, user_id: str, prefs: Dict[str, Any]):
        if user_id in self.users:
            self.users[user_id]["preferences"].update(prefs)

    def get_preferences(self, user_id: str) -> Dict[str, Any]:
        return self.users.get(user_id, {}).get("preferences", {})
