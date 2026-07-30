from starlette.requests import Request
from starlette.responses import JSONResponse
from fastmcp.server.dependencies import get_http_headers
from app.config import settings

def register_routes(mcp):
    @mcp.custom_route("/api/v1/.well-known/mcp.json", methods=["GET"])
    async def manifest(request: Request) -> JSONResponse:
        return JSONResponse({
            "name": settings.APP_TITLE,
            "version": settings.APP_VERSION
        })

    @mcp.custom_route("/api/v1/external-connection/me", methods=["GET"])
    async def connection_status(request: Request) -> JSONResponse:
        headers = get_http_headers()
        return JSONResponse({"connected": True})