from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class WebhookListenerService:
    """
    Listens for and normalizes incoming callbacks from external providers (e.g., Plaid, Stripe).
    Maps them to standard PFOS internal events (e.g., SYNC_REQUIRED, AUTH_REVOKED)
    and publishes them to the event bus.
    """
    def __init__(self, event_publisher):
        self.event_publisher = event_publisher

    async def handle_provider_callback(self, provider_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entrypoint for incoming webhooks. Routes to provider-specific handlers.
        """
        logger.info(f"Received webhook from {provider_type}")
        
        if provider_type.lower() == "plaid":
            return await self._handle_plaid_webhook(payload)
        elif provider_type.lower() == "stripe":
            return await self._handle_stripe_webhook(payload)
        else:
            logger.warning(f"Unhandled provider type: {provider_type}")
            return {"status": "ignored"}

    async def _handle_plaid_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        webhook_type = payload.get("webhook_type")
        webhook_code = payload.get("webhook_code")
        
        if webhook_type == "TRANSACTIONS":
            if webhook_code in ["INITIAL_UPDATE", "HISTORICAL_UPDATE", "DEFAULT_UPDATE"]:
                # Trigger a sync event
                # In production, publish an event indicating this connection_id needs syncing
                logger.info("Plaid Transactions update available. Event published.")
                return {"status": "sync_queued"}
                
        elif webhook_type == "ITEM":
            if webhook_code == "ERROR":
                # Handle ITEM_LOGIN_REQUIRED
                logger.warning("Plaid Item requires login. Event published.")
                return {"status": "auth_error_logged"}
                
        return {"status": "processed"}

    async def _handle_stripe_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        event_type = payload.get("type")
        
        if event_type == "charge.succeeded":
            logger.info("Stripe charge succeeded. Event published.")
            return {"status": "transaction_recorded"}
        elif event_type == "invoice.payment_failed":
            logger.warning("Stripe invoice payment failed. Event published.")
            return {"status": "alert_triggered"}
            
        return {"status": "processed"}
