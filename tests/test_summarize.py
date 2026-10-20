"""M1 /summarize 接口用例。"""
import pytest
from fastapi.testclient import TestClient
from httpx import Response


def _assert_validation_error(resp: Response, field: str) -> None:
    """断言请求返回 422，并且校验错误指向指定字段。"""
    assert resp.status_code == 422, (
        f"期望 422，实际 {resp.status_code}，响应：{resp.text}"
    )
    details = resp.json().get("detail")
    assert isinstance(details, list) and details, (
        f"422 响应的 detail 不是非空列表：{resp.text}"
    )
    assert any(
        item.get("loc", [])[-1:] == [field]
        for item in details
        if isinstance(item, dict)
    ), f"校验错误未指向字段 {field}：{details}"


@pytest.mark.api
def test_summarize_mock_success(client: TestClient):
    """正常文本按指定句数返回 mock 摘要。"""
    text = "第一句。第二句！第三句？第四句。"
    resp = client.post(
        "/summarize",
        json={"text": text, "max_sentences": 2},
    )

    assert resp.status_code == 200, (
        f"期望 200，实际 {resp.status_code}，响应：{resp.text}"
    )
    assert resp.json() == {
        "summary": "第一句。第二句！",
        "input_chars": len(text),
        "max_sentences": 2,
        "provider": "mock",
    }, f"摘要响应不符合契约：{resp.json()}"


@pytest.mark.api
def test_summarize_uses_default_sentence_limit(client: TestClient):
    """未传 max_sentences 时默认最多返回三句。"""
    text = "第一句。第二句。第三句。第四句。"
    resp = client.post("/summarize", json={"text": text})

    assert resp.status_code == 200, (
        f"期望 200，实际 {resp.status_code}，响应：{resp.text}"
    )
    body = resp.json()
    assert body["summary"] == "第一句。第二句。第三句。", (
        f"默认摘要句数错误：{body}"
    )
    assert body["max_sentences"] == 3, f"默认 max_sentences 错误：{body}"


@pytest.mark.api
@pytest.mark.parametrize(
    ("max_sentences", "expected"),
    [
        (1, "第一句。"),
        (5, "第一句。第二句。第三句。第四句。"),
    ],
    ids=["lower-boundary", "upper-boundary"],
)
def test_summarize_sentence_limit_boundaries(
    client: TestClient,
    max_sentences: int,
    expected: str,
):
    """max_sentences 的合法边界值可以被正确处理。"""
    text = "第一句。第二句。第三句。第四句。"
    resp = client.post(
        "/summarize",
        json={"text": text, "max_sentences": max_sentences},
    )

    assert resp.status_code == 200, (
        f"期望 200，实际 {resp.status_code}，响应：{resp.text}"
    )
    assert resp.json()["summary"] == expected, f"边界摘要错误：{resp.json()}"


@pytest.mark.api
@pytest.mark.parametrize(
    "text",
    ["", " \n\t "],
    ids=["empty", "whitespace-only"],
)
def test_summarize_rejects_blank_text(client: TestClient, text: str):
    """空文本和纯空白文本返回 422。"""
    resp = client.post("/summarize", json={"text": text})

    _assert_validation_error(resp, "text")


@pytest.mark.api
def test_summarize_rejects_text_without_words_or_numbers(client: TestClient):
    """只有标点的文本返回 422，避免摘要逻辑发生空句段错误。"""
    resp = client.post("/summarize", json={"text": "。！？..."})

    _assert_validation_error(resp, "text")


@pytest.mark.api
def test_summarize_rejects_text_over_2000_characters(client: TestClient):
    """超过 2000 字符的文本返回 422。"""
    resp = client.post("/summarize", json={"text": "字" * 2001})

    _assert_validation_error(resp, "text")


@pytest.mark.api
def test_summarize_accepts_2000_characters(client: TestClient):
    """恰好 2000 字符的文本属于合法输入。"""
    text = "字" * 2000
    resp = client.post("/summarize", json={"text": text})

    assert resp.status_code == 200, (
        f"期望 200，实际 {resp.status_code}，响应：{resp.text}"
    )
    assert resp.json()["input_chars"] == 2000, f"输入长度统计错误：{resp.json()}"


@pytest.mark.api
@pytest.mark.parametrize(
    "max_sentences",
    [0, 6],
    ids=["below-minimum", "above-maximum"],
)
def test_summarize_rejects_invalid_sentence_limit(
    client: TestClient,
    max_sentences: int,
):
    """max_sentences 超出 1~5 时返回 422。"""
    resp = client.post(
        "/summarize",
        json={"text": "第一句。", "max_sentences": max_sentences},
    )

    _assert_validation_error(resp, "max_sentences")


@pytest.mark.api
def test_summarize_requires_text_field(client: TestClient):
    """缺少 text 字段时返回 422。"""
    resp = client.post("/summarize", json={"max_sentences": 2})

    _assert_validation_error(resp, "text")
