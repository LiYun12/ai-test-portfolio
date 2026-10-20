"""AI 摘要与分类服务 —— 作品集被测系统。

M0 只有骨架接口；M1 起逐步加入 /summarize（mock + 真实模型）、
/classify（判断接口）与 /auth（鉴权）。
"""
import re
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="AI Test Portfolio Service",
    description="自研被测服务：接口测试、Web 自动化与 AI 测试的共同靶场。",
    version="0.1.0",
)


class SummarizeRequest(BaseModel):
    """摘要接口请求体。"""

    text: str = Field(min_length=1, max_length=2000)
    max_sentences: int = Field(default=3, ge=1, le=5)

    @field_validator("text")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        """拒绝空白文本和不含文字、数字的文本。"""
        normalized = value.strip()
        if not any(character.isalnum() for character in normalized):
            raise ValueError("text 至少包含一个文字或数字")
        return normalized


class SummarizeResponse(BaseModel):
    """摘要接口响应体。"""

    summary: str
    input_chars: int = Field(ge=0)
    max_sentences: int = Field(ge=1, le=5)
    provider: Literal["mock"] = "mock"


_SENTENCE_PATTERN = re.compile(r"[^.!?。！？]+[.!?。！？]*")


@app.get("/health")
def health() -> dict:
    """健康检查。"""
    return {"status": "ok"}


@app.get("/")
def index() -> dict:
    """服务基本信息。"""
    return {"service": "ai-test-portfolio", "version": "0.1.0"}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(payload: SummarizeRequest) -> SummarizeResponse:
    """返回确定性的 mock 摘要，供接口自动化测试使用。"""
    sentence_matches = list(_SENTENCE_PATTERN.finditer(payload.text))
    selected_matches = sentence_matches[: payload.max_sentences]
    summary_end = selected_matches[-1].end()
    summary = payload.text[:summary_end].strip()

    return SummarizeResponse(
        summary=summary,
        input_chars=len(payload.text),
        max_sentences=payload.max_sentences,
    )
