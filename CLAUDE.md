# English Buddy

幼儿英语启蒙 CLI 助手，帮助中文父母用地道童趣英语描述生活场景。

## 技术栈
- Python 3.12, Pydantic 2, Rich, FastAPI
- Google Gemini API (google-genai SDK)
- 前端：单文件 HTML + Tailwind CSS (CDN)
- 模型和 API Key 通过 `.env` 配置

## 项目结构
- `english_buddy/llm.py` — 核心业务逻辑，调用 Gemini API，返回结构化数据
- `english_buddy/cli.py` — 终端展示层（Rich）
- `english_buddy/api.py` — Web 展示层（FastAPI），API 端点 + 静态文件服务
- `english_buddy/static/index.html` — Web 前端页面
- `english_buddy/models.py` — Pydantic 响应模型
- `english_buddy/prompts.py` — System Prompt
- `english_buddy/config.py` — 从 .env 加载配置

## 常用命令
```bash
source .venv/bin/activate
# CLI 交互模式
python -m english_buddy
# CLI 单次查询
python -m english_buddy "场景描述"
# Web 服务（http://localhost:8000）
english-buddy-web
```

## 约定
- 业务逻辑层返回 Pydantic 模型，展示层（CLI/Web）负责渲染，严格分离
- 新增功能时保持分层：models → llm → (cli / api) → 入口
- API 端点统一在 `/api/` 下，返回 JSON，方便外部集成（Gem/Agent/微信）
- .env 不提交到 git，敏感信息只放 .env
