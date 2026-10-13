"""AI 摘要与分类服务 —— 作品集被测系统。

M0 只有骨架接口；M1 起逐步加入 /summarize（mock + 真实模型）、
/classify（判断接口）与 /auth（鉴权）。
"""
from fastapi import FastAPI

app = FastAPI(
    title="AI Test Portfolio Service",
    description="自研被测服务：接口测试、Web 自动化与 AI 测试的共同靶场。",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict:
    """健康检查。"""
    return {"status": "ok"}


@app.get("/")
def index() -> dict:
    """服务基本信息。"""
    return {"service": "ai-test-portfolio", "version": "0.1.0"}
