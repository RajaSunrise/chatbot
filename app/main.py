"""
Main FastAPI application for chatbot
"""
from fastapi import FastAPI
from api.main import router
from template import template

app = FastAPI(
    title="chatbot UTM",
    description="An open source Python AI assistant",
    version="0.1.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

app.include_router(router, prefix="/api/v1")
app.include_router(template.router, tags=["Template"])


