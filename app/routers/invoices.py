from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import SessionLocal
from ..services.invoice_service import FiscalServiceGateway, authorize_invoice

router = APIRouter(prefix="/invoices", tags=["invoices"])


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_gateway() -> FiscalServiceGateway:
    return FiscalServiceGateway()


@router.post("/", response_model=schemas.InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(invoice: schemas.InvoiceCreate, session: Session = Depends(get_session)):
    try:
        return crud.create_invoice(session, invoice)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/", response_model=list[schemas.InvoiceRead])
def list_invoices(session: Session = Depends(get_session)):
    return crud.list_invoices(session)


@router.post("/{invoice_id}/authorize", response_model=schemas.InvoiceRead)
def authorize(
    invoice_id: int,
    session: Session = Depends(get_session),
    gateway: FiscalServiceGateway = Depends(get_gateway),
):
    try:
        return authorize_invoice(session, invoice_id, gateway)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - general error mapping
        raise HTTPException(status_code=502, detail=str(exc)) from exc
