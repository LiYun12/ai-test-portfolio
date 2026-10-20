# AI Test Portfolio

个人测试开发作品集：自研被测服务 + 接口自动化 + Web 自动化 + CI。

路线：自动化测试 → AI 测试 → 测试专家。阶段计划见 `docs/roadmap.md`。

项目目标、当前进度、目录结构和下一步任务统一记录在
[`docs/project-guide.md`](docs/project-guide.md)。

## 目录结构

```text
ai-test-portfolio/
├── app/            # 被测服务（FastAPI）
├── tests/          # pytest 用例
├── docs/           # 路线图、学习日志
├── pytest.ini
└── requirements.txt
```

## 快速开始（Windows PowerShell）

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest                              # 跑全部用例
uvicorn app.main:app --reload       # 起服务，浏览器打开 http://127.0.0.1:8000/docs
```

## API

- `GET /health`：健康检查；
- `GET /`：服务基本信息；
- `POST /summarize`：mock 摘要接口，文本限制 1~2000 字符且至少包含一个文字或数字，摘要句数限制 1~5。

摘要请求示例：

```json
{
  "text": "第一句。第二句！第三句？",
  "max_sentences": 2
}
```

## 工作约定

- 断言必须带失败信息：`assert actual == expected, "说明"`，禁止裸 assert；
- 账号、密钥一律走环境变量，代码与文档里零真实凭据；
- commit 前缀：`feat:` / `test:` / `docs:` / `fix:`；
- 每天收工：一次 commit + 一行日志（`docs/learning-log.md`）。
