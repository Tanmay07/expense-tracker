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
