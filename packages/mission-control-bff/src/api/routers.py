from fastapi import APIRouter, Header, Depends
from src.services.aggregator import BFFAggregatorService

router = APIRouter(prefix="/api/bff")


def get_aggregator():
    return BFFAggregatorService()


@router.get("/dashboard")
async def get_dashboard(
    user_id: str = Header("mock_user_123"),
    agg: BFFAggregatorService = Depends(get_aggregator),
):
    return await agg.get_dashboard_data(user_id)


@router.get("/timeline")
async def get_timeline(
    user_id: str = Header("mock_user_123"),
    agg: BFFAggregatorService = Depends(get_aggregator),
):
    return await agg.get_timeline_feed(user_id)


@router.get("/missions")
async def get_missions(
    user_id: str = Header("mock_user_123"),
    agg: BFFAggregatorService = Depends(get_aggregator),
):
    return await agg.get_mission_center(user_id)


@router.get("/graph")
async def get_graph(
    user_id: str = Header("mock_user_123"),
    agg: BFFAggregatorService = Depends(get_aggregator),
):
    return await agg.get_graph_data(user_id)


from mission_control.application.services.context_service import (  # noqa: E402
    ContextWorkspaceService,
    AdaptiveDashboardService,
    AdaptiveActionService,
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


from mission_control.application.services.workspace_service import WorkspaceService  # noqa: E402


@router.get("/workspaces")
async def get_workspaces(user_id: str = Header("mock_user_123")):
    service = WorkspaceService()
    workspaces = service.get_all_workspaces(user_id)
    return {"workspaces": [ws.model_dump() for ws in workspaces]}


@router.get("/workspaces/{workspace_id}")
async def get_workspace(workspace_id: str, user_id: str = Header("mock_user_123")):
    service = WorkspaceService()
    workspace = service.get_workspace(workspace_id, user_id)
    return workspace.model_dump()


from mission_control.application.services.ai_service import (  # noqa: E402
    ToolRegistryService,
    CapabilityRegistryService,
)


@router.get("/ai/capabilities")
async def get_ai_capabilities():
    service = CapabilityRegistryService()
    capabilities = service.list_capabilities()
    return {"capabilities": [c.model_dump() for c in capabilities]}


@router.get("/ai/tools")
async def get_ai_tools():
    service = ToolRegistryService()
    tools = service.list_tools()
    return {"tools": [t.model_dump() for t in tools]}


@router.post("/ai/chat")
async def ai_chat(payload: dict, user_id: str = Header("mock_user_123")):
    return {"reply": "This is a response from the AI BFF.", "tool_invocations": []}


@router.get("/ai/conversations")
async def get_conversations(user_id: str = Header("mock_user_123")):
    return {"conversations": []}


@router.get("/ai/context")
async def get_ai_context(user_id: str = Header("mock_user_123")):
    return {"context": {}}


@router.post("/ai/context/preview")
async def preview_ai_context(payload: dict, user_id: str = Header("mock_user_123")):
    return {"preview": {}}


@router.get("/ai/capabilities/discover")
async def discover_capabilities(user_id: str = Header("mock_user_123")):
    service = CapabilityRegistryService()
    return {"capabilities": [c.model_dump() for c in service.list_capabilities()]}


@router.get("/ai/capabilities/{capability_id}")
async def get_capability(capability_id: str, user_id: str = Header("mock_user_123")):
    service = CapabilityRegistryService()
    cap = service.get_capability(capability_id)
    return cap.model_dump() if cap else {}


@router.get("/ai/capabilities/availability")
async def get_capability_availability(user_id: str = Header("mock_user_123")):
    return {"available": True}


@router.get("/ai/tools/discover")
async def discover_tools(user_id: str = Header("mock_user_123")):
    service = ToolRegistryService()
    return {"tools": [t.model_dump() for t in service.list_tools()]}


@router.get("/ai/approvals")
async def get_approvals(user_id: str = Header("mock_user_123")):
    return {"approvals": []}


@router.get("/ai/replay")
async def get_replays(user_id: str = Header("mock_user_123")):
    return {"replays": []}


@router.get("/ai/widgets")
async def get_ai_widgets(user_id: str = Header("mock_user_123")):
    return {"widgets": []}


@router.get("/ai/history")
async def get_ai_history(user_id: str = Header("mock_user_123")):
    return {"history": []}


@router.post("/ai/multimodal")
async def process_multimodal(payload: dict, user_id: str = Header("mock_user_123")):
    return {"status": "processed"}


@router.post("/ai/upload")
async def ai_upload(user_id: str = Header("mock_user_123")):
    return {"status": "uploaded"}


@router.post("/ai/export")
async def ai_export(payload: dict, user_id: str = Header("mock_user_123")):
    return {"status": "exported"}


@router.post("/ai/search")
async def ai_search(payload: dict, user_id: str = Header("mock_user_123")):
    return {"results": []}


@router.get("/ai/insights")
async def get_ai_insights(user_id: str = Header("mock_user_123")):
    return {"insights": []}


@router.post("/ai/telemetry")
async def ai_telemetry(payload: dict, user_id: str = Header("mock_user_123")):
    # Receives OpenTelemetry/Observability data from the UI
    return {"status": "recorded"}
