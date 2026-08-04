from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.database import Base, engine
from app.routers import categories, expenses

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Budget Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production via env-driven allowlist
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router)
app.include_router(expenses.router)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/api/health")
def health():
    return {"status": "ok"}
