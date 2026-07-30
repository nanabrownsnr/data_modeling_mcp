from fastmcp import FastMCP
from fastmcp.apps import AppConfig, ResourceCSP
from fastmcp.tools import ToolResult

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from pathlib import Path
from typing import Any, Optional

class NodeData(BaseModel):
    label: str

class Node(BaseModel):
    id: str
    data: NodeData

class Edge(BaseModel):
    id: str
    source: str
    target: str

mcp = FastMCP(
    "data_modeling_mcp"
    )

VIEW_URI = "ui://data_model_mcp/view.html"

VIEW_HTML = (
    Path(__file__).parent 
    / "views"
    / "dist"
    / "index.html"
).read_text()

@mcp.resource(
    VIEW_URI,
    app=AppConfig()
)
def data_model_view():
    return VIEW_HTML


@mcp.tool(
    app=AppConfig(resource_uri=VIEW_URI)
)
def render_data_model(nodes: list[Node], edges: list[Edge]):
    """
    Render an entity-relationship style data model on the data modeling canvas.

    This tool accepts a list of nodes and edges that describe a graph and
    forwards them to the front-end view for visualization. Each node
    represents an entity (for example, a table or domain object) and each
    edge represents a relationship between two entities.

    Parameters
    ----------
    nodes : list[Node]
        The nodes to render. Each node must have a unique `id` and a `data`
        payload containing at least a `label` field used as the display name
        in the diagram.

    edges : list[Edge]
        The edges to render. Each edge must have a unique `id`, a `source`
        node ID, and a `target` node ID that reference existing nodes.
    """

    structured = {
        "nodes": [n.model_dump() for n in nodes],
        "edges": [e.model_dump() for e in edges]
    }


    return ToolResult(
        content=f"rendered this data on the canvas: {structured}",
        structured_content=structured
        # meta={"ui": {"resourceUri": VIEW_URI}, "ui/resourceUri": VIEW_URI}
    )

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["mcp-protocol-version", "Authorization", "Content-Type"]
        # allow_headers=["mcp-protocol-version", "mcp-session-id", "Authorization", "Content-Type"],
        # expose_headers=["mcp-session-id"],
    )
]

app = mcp.http_app(middleware=middleware)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)