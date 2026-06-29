from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import asyncio
import json

from .dependencies import get_mission_control_service, get_opportunity_service, get_risk_service
from ..application.services import MissionControlService, OpportunityService, RiskService
from ..domain.models import Mission, Opportunity, Risk

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.get("/missions", response_model=List[Mission])
def get_missions(
    user_id: str,
    service: MissionControlService = Depends(get_mission_control_service)
):
    return service.get_user_feed(user_id)

@router.post("/opportunities/detect", response_model=List[Opportunity])
def detect_opportunities(
    user_id: str,
    service: OpportunityService = Depends(get_opportunity_service)
):
    return service.detect_opportunities(user_id)

@router.post("/risks/detect", response_model=List[Risk])
def detect_risks(
    user_id: str,
    service: RiskService = Depends(get_risk_service)
):
    return service.detect_risks(user_id)

@router.websocket("/ws/mission-feed/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket)
    try:
        while True:
            # In a real system, this would listen to Redis PubSub or similar message bus
            # Here we mock periodic live updates to the client
            await asyncio.sleep(10)
            update = {"type": "FEED_UPDATE", "timestamp": str(asyncio.get_event_loop().time())}
            await websocket.send_text(json.dumps(update))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
