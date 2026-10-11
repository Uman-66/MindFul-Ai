"""This will create the FastAPI application and register routers."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import ALLOWED_ORIGINS
from .routers import analyze, chat, config_router, fuse, health, plan, reports, resources
app = FastAPI(title="MindPulse AI", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=[item for item in ALLOWED_ORIGINS.split(",") if item] or ["*"], allow_methods=["*"], allow_headers=["*"])
for router in (health.router, config_router.router, analyze.router, fuse.router, resources.router, plan.router, reports.router, chat.router): app.include_router(router, prefix="/api/v1")
