"""Create and configure the BackToU FastAPI application."""

from fastapi import FastAPI

from app.api.routes import auth, health


app = FastAPI(title="BackToU API")

app.include_router(health.router)
app.include_router(auth.router)
