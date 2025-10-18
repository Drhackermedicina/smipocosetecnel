from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import SessionLocal
from ..services.alert_service import purge_expired_alerts

router = APIRouter(prefix="/alerts", tags=["alerts"])


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.get("/", response_model=list[schemas.AlertRead])
def list_alerts(session: Session = Depends(get_session)):
    purge_expired_alerts(session)
    return crud.list_alerts(session)


@router.post("/", response_model=schemas.AlertRead, status_code=status.HTTP_201_CREATED)
def create_alert(alert: schemas.AlertCreate, session: Session = Depends(get_session)):
    return crud.create_alert(session, alert)


@router.post("/{alert_id}/resolve", response_model=schemas.AlertRead)
def resolve_alert(alert_id: int, session: Session = Depends(get_session)):
    alert = crud.resolve_alert(session, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    return alert
