# tests/test_auth.py
import pytest
from starlette.testclient import TestClient
from fastmcp import FastMCP
from app.twynity import register_routes
from app.auth import get_auth_provider


@pytest.fixture
def authenticated_app():
    mcp = FastMCP("test_server", auth=get_auth_provider())
    register_routes(mcp)
    return mcp.http_app()
