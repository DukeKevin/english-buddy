# English Buddy

幼儿英语启蒙助手（CLI + Web + 微信公众号），帮助中文父母用地道童趣英语描述生活场景。

## 技术栈
- Python 3.12, Pydantic 2, Rich, FastAPI
- Google Gemini API (google-genai SDK)
- 前端：单文件 HTML + Tailwind CSS (CDN)
- 模型和 API Key 通过 `.env` 配置

## 项目结构
- `english_buddy/llm.py` — 核心业务逻辑，调用 Gemini API，返回结构化数据
- `english_buddy/cli.py` — 终端展示层（Rich）
- `english_buddy/api.py` — Web 展示层（FastAPI），API 端点 + 静态文件服务
- `english_buddy/wechat.py` — 微信公众号 webhook 路由
- `english_buddy/store.py` — 内存结果存储（微信异步查询用）
- `english_buddy/static/index.html` — Web 前端页面
- `english_buddy/static/result.html` — 微信结果展示页（带轮询 + TTS）
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
# 公网隧道（微信 webhook 需要）
cloudflared tunnel --url http://localhost:8000
```

## 微信公众号集成
- 用户在微信发送中文场景描述 → webhook 立即回复结果链接 → 后台异步调 Gemini → 用户点链接查看结果
- 立即回复链接绕过微信 5 秒超时限制
- 微信 MsgId 去重，防止超时重试产生重复查询
- 公众号后台服务器配置：URL 填 `{BASE_URL}/wechat`，Token 填 `.env` 中的 `WECHAT_TOKEN`
- 开发阶段用 cloudflared quick tunnel 暴露本地端口，每次重启域名会变，需同步更新 `.env` 的 `BASE_URL` 和公众号后台配置

## 约定
- 业务逻辑层返回 Pydantic 模型，展示层（CLI/Web）负责渲染，严格分离
- 新增功能时保持分层：models → llm → (cli / api) → 入口
- API 端点统一在 `/api/` 下，返回 JSON，方便外部集成（Gem/Agent/微信）
- .env 不提交到 git，敏感信息只放 .env
