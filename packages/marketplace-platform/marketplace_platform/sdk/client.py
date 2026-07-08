import httpx
from typing import Dict, Any, List, Optional


class MarketplaceSDK:
    """
    SDK for the Enterprise Decision Marketplace & Strategy Exchange Platform.
    Allows other modules to discover and consume governed reusable financial assets.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(base_url=self.base_url)

    def getAsset(self, asset_id: str) -> Dict[str, Any]:
        resp = self.client.get(f"/marketplace/assets/{asset_id}")
        resp.raise_for_status()
        return resp.json()

    def listAssets(self, asset_type: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if asset_type:
            params["asset_type"] = asset_type
        resp = self.client.get("/marketplace/assets", params=params)
        resp.raise_for_status()
        return resp.json()

    def checkAiUsability(self, asset_id: str, ai_consumer: str) -> bool:
        resp = self.client.get(
            f"/marketplace/assets/{asset_id}/usability",
            params={"ai_consumer": ai_consumer},
        )
        resp.raise_for_status()
        return resp.json()

    def publishAsset(self, dto: Dict[str, Any]) -> Dict[str, Any]:
        resp = self.client.post("/marketplace/assets", json=dto)
        resp.raise_for_status()
        return resp.json()

    def deprecateAsset(self, asset_id: str, reason: str) -> Dict[str, Any]:
        resp = self.client.post(
            f"/marketplace/assets/{asset_id}/deprecate", params={"reason": reason}
        )
        resp.raise_for_status()
        return resp.json()

    def certifyAsset(
        self, asset_id: str, certifier_id: str, tier: str
    ) -> Dict[str, Any]:
        params = {"certifier_id": certifier_id, "tier": tier}
        resp = self.client.post(
            f"/marketplace/assets/{asset_id}/certify", params=params
        )
        resp.raise_for_status()
        return resp.json()
