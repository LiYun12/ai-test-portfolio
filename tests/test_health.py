"""M0 基础路由用例：健康检查与服务信息。"""
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """GET /health 返回 200 且状态为 ok。"""
    resp = client.get("/health")
    assert resp.status_code == 200, (
        f"期望 200，实际 {resp.status_code}，响应：{resp.text}"
    )
    body = resp.json()
    assert body.get("status") == "ok", f"health 状态异常，响应体：{body}"


def test_index_info(client: TestClient):
    """GET / 返回服务名称与版本。"""
    resp = client.get("/")
    assert resp.status_code == 200, (
        f"期望 200，实际 {resp.status_code}，响应：{resp.text}"
    )
    body = resp.json()
    assert body.get("service") == "ai-test-portfolio", (
        f"service 字段缺失或错误：{body}"
    )
    assert body.get("version") == "0.1.0", f"version 字段缺失或错误：{body}"
