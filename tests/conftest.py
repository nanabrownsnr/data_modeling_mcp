import pytest
from unittest.mock import AsyncMock, patch


@pytest.fixture
def mock_jwks():
    """Fake JWKS response so tests don't hit the real Account Service."""
    fake_keys = {"keys": [{"kid": "test-key", "kty": "RSA", "n": "fake", "e": "AQAB"}]}
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.json.return_value = fake_keys
        mock_get.return_value.raise_for_status = lambda: None
        yield mock_get


@pytest.fixture
def sample_nodes_edges():
    """Reusable sample payload for tool tests."""
    return {
        "nodes": [
            {"id": "n1", "data": {"label": "Users"}},
            {"id": "n2", "data": {"label": "Orders"}},
        ],
        "edges": [
            {"id": "e1", "source": "n1", "target": "n2"},
        ],
    }