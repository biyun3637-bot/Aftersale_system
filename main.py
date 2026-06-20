"""Entry point: FastAPI app + static files + frontend templates."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

import config
from web.routes import router as api_router
import db

db.init_db()


app = FastAPI(
    title="AI Agent + RPA - Cross-border After-sale System",
    debug=True,
    version="1.0.0",
    description="Cross-border e-commerce after-sale refund + abnormal order auto-processing system Demo",
)

app.include_router(api_router, prefix="/api")

static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

template_dir = os.path.join(os.path.dirname(__file__), "web", "templates")


@app.get("/", response_class=HTMLResponse)
def showcase():
    with open(os.path.join(template_dir, "showcase.html"), "r", encoding="utf-8") as f:
        return f.read()


@app.get("/demo", response_class=HTMLResponse)
def demo():
    with open(os.path.join(template_dir, "dashboard.html"), "r", encoding="utf-8") as f:
        return f.read()


@app.get("/review", response_class=HTMLResponse)
def review_page():
    with open(os.path.join(template_dir, "review.html"), "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    print(f" Demo running at http://{config.HOST}:{config.PORT}")
    print(f"   DEMO_MODE={config.DEMO_MODE}")
    print(f"   LLM_PROVIDER={config.LLM_PROVIDER}")
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=False)