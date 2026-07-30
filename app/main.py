
import asyncio

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import Middleware as MCPMiddleware, MiddlewareContext

from app.config import settings
from app.auth import get_auth_provider
from app.license import license_watcher
from app.tools.render_data_model_tool import register_tools
from app.resources.view_resource import register_resources
from app.twynity import register_routes
from app.usage import save_usage_report


@asynccontextmanager
async def app_lifespan(server):
    task = asyncio.create_task(license_watcher())
    yield
    task.cancel()

mcp = FastMCP(
    settings.APP_TITLE,
    auth=get_auth_provider(),
    lifespan=app_lifespan,
)


register_tools(mcp)
class UsageTrackingMiddleware(MCPMiddleware):
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        headers = get_http_headers()
        await save_usage_report(
            method="TOOL_CALL",
            endpoint=context.message.name,
            auth_header=headers.get("authorization"),
        )
        return await call_next(context)
mcp.add_middleware(UsageTrackingMiddleware())

register_resources(mcp)
register_routes(mcp)


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["https://staging.twynity.ai", "https://dev.twynity.ai"],
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["mcp-protocol-version", "mcp-session-id", "Authorization", "Content-Type"],
        expose_headers=["mcp-session-id"],
    )
]


app = mcp.http_app(middleware=middleware)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)