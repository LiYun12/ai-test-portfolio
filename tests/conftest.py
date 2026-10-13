"""pytest 共享 fixture。"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """会话级 API 客户端：无需先启动 uvicorn。"""
    return TestClient(app)
