from fastmcp.server.auth.providers.jwt import JWTVerifier
from app.config import settings

def get_auth_provider() -> JWTVerifier:
    """Builds the auth checker FastMCP will run on every incoming request."""
    return JWTVerifier(
        jwks_uri=settings.ACCOUNT_SERVICE_URL,
        audience=settings.SERVICE_ID,
    )