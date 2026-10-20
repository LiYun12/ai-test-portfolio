# AI Test Portfolio 项目导航

> 忘记这个项目要做什么时，先看这份文档。当前只推进本文件列出的任务，不临时增加新技术或新方向。

## 1. 一句话说明

这是一个用于求职的测试开发作品集：先自己开发一个带 AI 功能的 FastAPI 服务，再围绕它完成接口自动化、Web 自动化、CI 和 AI 测试实验。

它不是课程练习集合，也不是单纯刷题项目。最终要证明四件事：

1. 能使用 Python 和 FastAPI 开发一个可测试的服务；
2. 能使用 pytest、requests、Allure 建立接口自动化体系；
3. 能使用 Playwright + POM 建立 Web 自动化体系；
4. 能对 AI 输出进行可重复的评测，而不只是调用模型接口。

## 2. 最终交付物

到 M4 结束时，仓库应包含：

- FastAPI 被测服务：`/health`、`/summarize`、`/classify`、`/auth`；
- 15~20 条接口自动化用例，覆盖正常流、异常流、边界和鉴权；
- Allure 测试报告；
- Playwright + POM Web 自动化用例和失败截图；
- GitHub Actions CI；
- `/classify` 的 AI 判断实验：金标集、准确率、置信度和阈值分析；
- 可读的 README、演示录屏和可用于面试讲解的项目说明。

## 3. 当前目录结构

```text
ai-test-portfolio/
├── app/
│   ├── __init__.py
│   └── main.py              # FastAPI 服务入口
├── tests/
│   ├── conftest.py          # pytest 共享 fixture
│   └── test_health.py       # 健康检查、首页和 404 用例
├── docs/
│   ├── project-guide.md     # 当前这份项目导航
│   ├── roadmap.md           # 里程碑和截止时间
│   └── learning-log.md      # 每日学习记录
├── README.md
├── pytest.ini
└── requirements.txt
```

后续只会按里程碑需要增加目录，例如 API/UI 分层、测试数据、Allure 报告和 `.github/workflows/`，不会为了“看起来专业”提前堆结构。

## 4. 当前进度

更新时间：2026-10-20

- M0 已完成：仓库、FastAPI 骨架、3 条基础用例、GitHub SSH 和首次推送；
- 当前测试：`3 passed`；
- 当前分支：`main`，已跟踪 `origin/main`；
- 当前提交：`bb8d486 test:完善未知路由404响应断言`；
- M1 正在进行：下一步是 `/summarize` 的 mock 接口和边界用例；
- 已知但不阻塞的问题：FastAPI/Starlette 的 TestClient 产生 `httpx` 弃用警告。

## 5. 接下来要做什么

只按以下顺序做，完成一项再做下一项：

### 任务 1：`POST /summarize`

- 建立请求和响应模型；
- 默认返回 mock 结果，不调用真实模型；
- 校验空文本、纯空白、超长文本和句数范围；
- 新增 6~8 条原子 API 用例；
- 跑绿后提交一次。

### 任务 2：`POST /classify`

- 输入一段文本，返回分类和置信度；
- 先使用确定性 mock 规则；
- 覆盖合法分类、非法输入、低置信度阈值；
- 新增 5~6 条 API 用例。

### 任务 3：`/auth`

- 凭据只从环境变量读取，禁止写进代码和测试数据；
- 覆盖无凭据、错误凭据、正确凭据和权限不足；
- 新增 3~5 条鉴权用例。

### 任务 4：Allure

- 统一测试命令；
- 生成可打开的 Allure 报告；
- 确认 M1 的 15~20 条用例可以一条命令跑完。

## 6. 每天的固定流程

1. 只选择一个最小任务，例如“实现 /summarize 的正常响应”；
2. 写实现或测试，不边做边学完整课程；
3. 运行全部测试；
4. 更新 `docs/learning-log.md` 一行；
5. 提交并推送；
6. 卡住超过 30 分钟就记录欠账，先换到可完成的部分。

常用命令：

```powershell
cd D:\AI\Codex\Design\ai-test-portfolio
.\.venv\Scripts\Activate.ps1
python -m pytest -q -p no:cacheprovider
git status
git add .
git commit -m "test: 说明本次改动"
git push
```

启动服务并查看接口文档：

```powershell
uvicorn app.main:app --reload
```

浏览器打开 `http://127.0.0.1:8000/docs`。

## 7. 完成标准

一个任务只有同时满足以下条件才算完成：

- 行为符合接口契约；
- 正常、边界和异常场景都有测试；
- 断言包含明确失败信息；
- 全部测试通过；
- 学习日志已更新；
- 代码已提交并推送；
- README 或接口说明在行为变化时已同步。

## 8. 迷路时执行这三步

1. 打开本文件的“当前进度”和“接下来要做什么”；
2. 只选择当前里程碑中的第一项未完成任务；
3. 如果想法属于 M2 或以后，记录到 `docs/roadmap.md`，现在不执行。

## 9. 相关文档

- [路线图](roadmap.md)
- [学习日志](learning-log.md)
- [项目首页](../README.md)
