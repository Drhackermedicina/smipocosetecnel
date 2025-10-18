from __future__ import annotations

import random
from datetime import datetime

from sqlalchemy.orm import Session

from .. import crud, models


class FiscalIntegrationError(RuntimeError):
    """Raised when the mock fiscal integration fails."""


class FiscalServiceGateway:
    """Simulated gateway for Receita Federal/SEFAZ integration."""

    def transmit_invoice(self, invoice: models.Invoice) -> tuple[str, str]:
        """Pretend to transmit an invoice and return (key, xml).

        In a real-world scenario this method would:
        - Build an NF-e XML according to layout 4.0.
        - Sign it with a digital certificate (A1/A3).
        - Send it to the state's SEFAZ webservice and await authorization.

        Here we just simulate success/failure using pseudo randomness.
        """

        if random.random() < 0.1:
            raise FiscalIntegrationError("Falha de comunicação com SEFAZ simulada")

        document_key = f"{datetime.utcnow():%Y%m%d%H%M%S}{invoice.id:06d}"
        xml_payload = f"<NFe><infNFe Id=\"{document_key}\"></infNFe></NFe>"
        return document_key, xml_payload


def authorize_invoice(session: Session, invoice_id: int, gateway: FiscalServiceGateway) -> models.Invoice:
    invoice = session.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise ValueError("Nota fiscal não encontrada")

    document_key, xml_payload = gateway.transmit_invoice(invoice)
    return crud.mark_invoice_as_issued(session, invoice, document_key, xml_payload)
