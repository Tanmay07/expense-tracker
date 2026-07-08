from typing import List, Dict
from datetime import datetime
from ...domain.models.workspace import WorkspaceModel, WorkspaceSnapshot, WidgetConfig


class WorkspaceService:
    def __init__(self):
        # In a real app, this would use a repository to fetch from DB
        self._mock_workspaces = self._seed_workspaces()

    def _seed_workspaces(self) -> Dict[str, WorkspaceModel]:
        # Default workspaces to satisfy the "Financial Workspaces" module
        workspaces = [
            WorkspaceModel(
                id="ws_expenses",
                name="Expenses",
                description="Manage and analyze daily expenses",
                icon="CreditCard",
                path="/workspaces/expenses",
                is_default=True,
                snapshots=[
                    WorkspaceSnapshot(
                        id="snap_default_exp",
                        name="Default View",
                        created_at=datetime.utcnow(),
                        widgets=[
                            WidgetConfig(
                                id="w1",
                                widget_type="KPI",
                                title="Total Expenses",
                                data_source="expenses.total",
                                layout={"w": 3, "h": 1, "x": 0, "y": 0},
                            ),
                            WidgetConfig(
                                id="w2",
                                widget_type="CHART",
                                title="Spending by Category",
                                data_source="expenses.categories",
                                layout={"w": 9, "h": 2, "x": 3, "y": 0},
                            ),
                        ],
                        layout_config={"sidebar_width": 250, "inspector_width": 300},
                    )
                ],
            ),
            WorkspaceModel(
                id="ws_investments",
                name="Investments",
                description="Portfolio tracking and market analysis",
                icon="TrendingUp",
                path="/workspaces/investments",
            ),
        ]
        return {ws.id: ws for ws in workspaces}

    def get_all_workspaces(self, user_id: str) -> List[WorkspaceModel]:
        # Auth check would go here
        return list(self._mock_workspaces.values())

    def get_workspace(self, workspace_id: str, user_id: str) -> WorkspaceModel:
        if workspace_id not in self._mock_workspaces:
            raise ValueError(f"Workspace {workspace_id} not found")
        return self._mock_workspaces[workspace_id]

    def save_snapshot(
        self, workspace_id: str, snapshot: WorkspaceSnapshot, user_id: str
    ) -> WorkspaceModel:
        if workspace_id not in self._mock_workspaces:
            raise ValueError(f"Workspace {workspace_id} not found")

        ws = self._mock_workspaces[workspace_id]
        ws.snapshots.append(snapshot)
        ws.active_snapshot_id = snapshot.id
        return ws
