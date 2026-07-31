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
        }, status_code=200) 

    @mcp.custom_route("/api/v1/health", methods=["GET"])
    async def health_status(request: Request) -> JSONResponse:
        headers = get_http_headers()
        return JSONResponse({"status": "ok"}, status_code=200)