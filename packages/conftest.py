import os
import sys

# Add the workspace root to sys.path so 'src' can be imported by the IDE
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

# import pytest
# from src.main import app
# from src.presentation.api import get_current_user_id

# @pytest.fixture(autouse=True)
# def override_auth():
#     app.dependency_overrides[get_current_user_id] = lambda: "mock_user_123"
#     yield
#     app.dependency_overrides.clear()
