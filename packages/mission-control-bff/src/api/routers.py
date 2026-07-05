from fastapi import APIRouter, Header, Depends
from src.services.aggregator import BFFAggregatorService

router = APIRouter(prefix="/api/bff")

def get_aggregator():
    return BFFAggregatorService()

@router.get("/dashboard")
async def get_dashboard(
    user_id: str = Header("mock_user_123"), 
    agg: BFFAggregatorService = Depends(get_aggregator)
):
    return await agg.get_dashboard_data(user_id)

@router.get("/timeline")
async def get_timeline(
    user_id: str = Header("mock_user_123"), 
    agg: BFFAggregatorService = Depends(get_aggregator)
):
    return await agg.get_timeline_feed(user_id)

@router.get("/missions")
async def get_missions(
    user_id: str = Header("mock_user_123"), 
    agg: BFFAggregatorService = Depends(get_aggregator)
):
    return await agg.get_mission_center(user_id)

@router.get("/graph")
async def get_graph(
    user_id: str = Header("mock_user_123"), 
    agg: BFFAggregatorService = Depends(get_aggregator)
):
    return await agg.get_graph_data(user_id)

from mission_control.application.services.context_service import (
    ContextWorkspaceService,
    AdaptiveDashboardService,
    AdaptiveActionService
)

@router.get("/context")
async def get_active_context(user_id: str = Header("mock_user_123")):
    service = ContextWorkspaceService()
    contexts = service.get_active_contexts(user_id)
    return {"contexts": [c.model_dump() for c in contexts]}

@router.get("/dashboard/adaptive")
async def get_adaptive_dashboard(user_id: str = Header("mock_user_123")):
    context_service = ContextWorkspaceService()
    layout_service = AdaptiveDashboardService()
    
    contexts = context_service.get_active_contexts(user_id)
    layout = layout_service.get_dashboard_layout(user_id, contexts)
    return {"layout": layout}

@router.get("/quick-actions")
async def get_quick_actions(user_id: str = Header("mock_user_123")):
    context_service = ContextWorkspaceService()
    action_service = AdaptiveActionService()
    
    contexts = context_service.get_active_contexts(user_id)
    actions = action_service.get_quick_actions(user_id, contexts)
    return {"actions": [a.model_dump() for a in actions]}
