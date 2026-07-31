# tests/test_tools.py
import pytest
from fastmcp import FastMCP
from app.tools.render_data_model_tool import register_tools


@pytest.fixture
def mcp_instance():
    mcp = FastMCP("test_server")
    register_tools(mcp)
    return mcp


@pytest.mark.asyncio
async def test_render_data_model_returns_structured_content(mcp_instance, sample_nodes_edges):
    render_tool = await mcp_instance.get_tool("render_data_model")
    assert render_tool is not None

    result = await render_tool.run(sample_nodes_edges)

    assert result.structured_content["nodes"][0]["id"] == "n1"
    assert result.structured_content["edges"][0]["source"] == "n1"
    assert result.structured_content["edges"][0]["target"] == "n2"

