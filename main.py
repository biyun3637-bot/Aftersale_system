"""入口文件：FastAPI 应用 + 静态文件 + 前端模板。"""
import os
import sys

# 确保模块路径正确
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

import config
from web.routes import router as api_router
import db

# ━━ FastAPI 应用 ━━
# ━━ 数据库初始化（自动建表）━━
db.init_db()


app = FastAPI(
    title="AI Agent + RPA 混合架构 · 跨境售后系统",
    debug=True,
    version="1.0.0",
    description="跨境电商售后退款 + 异常订单自动处理系统 Demo",
)

# ━━ 注册 API 路由 ━━
app.include_router(api_router, prefix="/api")

# ━━ 挂载静态文件 ━━
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ━━ 前端页面（dashboard + review）━━
template_dir = os.path.join(os.path.dirname(__file__), "web", "templates")


@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open(os.path.join(template_dir, "dashboard.html"), "r", encoding="utf-8") as f:
        return f.read()


@app.get("/review", response_class=HTMLResponse)
def review_page():
    with open(os.path.join(template_dir, "review.html"), "r", encoding="utf-8") as f:
        return f.read()


# ━━ 启动 ━━
if __name__ == "__main__":
    print(f" Demo 启动: http://{config.HOST}:{config.PORT}")
    print(f"   DEMO_MODE={config.DEMO_MODE}")
    print(f"   LLM_PROVIDER={config.LLM_PROVIDER}")
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=False)
