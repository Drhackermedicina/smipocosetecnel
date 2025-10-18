from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models import Base
from .routers import alerts, invoices, partners, products

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SMI - Gestão de Materiais Elétricos e Hidráulicos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(partners.router)
app.include_router(products.router)
app.include_router(invoices.router)
app.include_router(alerts.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
