from __future__ import annotations

from datetime import datetime
from typing import Iterable

from sqlalchemy.orm import Session

from .. import crud, models


def purge_expired_alerts(session: Session) -> int:
    """Remove expired alerts from the active list."""
    alerts: Iterable[models.Alert] = crud.list_alerts(session, include_resolved=True)
    removed = 0
    for alert in alerts:
        if alert.expires_at and alert.expires_at < datetime.utcnow():
            session.delete(alert)
            removed += 1
    session.flush()
    return removed
