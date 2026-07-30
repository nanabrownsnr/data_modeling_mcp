from pathlib import Path
from fastmcp.apps import AppConfig

VIEW_URI = "ui://data_model_mcp/view.html"
VIEW_HTML = (Path(__file__).parent / "views" / "dist" / "index.html").read_text()

def register_resources(mcp):
    @mcp.resource(VIEW_URI, app=AppConfig())
    def data_model_view():
        return VIEW_HTML