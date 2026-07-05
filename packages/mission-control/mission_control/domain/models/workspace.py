from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class WidgetConfig(BaseModel):
    id: str
    widget_type: str # 'CHART', 'KPI', 'NOTE', 'TABLE', 'AI_CARD'
    title: str
    data_source: str
    layout: Dict[str, Any] = Field(default_factory=lambda: {"w": 4, "h": 2, "x": 0, "y": 0})
    settings: Dict[str, Any] = Field(default_factory=dict)

class WorkspaceSnapshot(BaseModel):
    id: str
    name: str
    created_at: datetime
    widgets: List[WidgetConfig]
    layout_config: Dict[str, Any]

class WorkspaceModel(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    path: str
    is_default: bool = False
    active_snapshot_id: Optional[str] = None
    snapshots: List[WorkspaceSnapshot] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
