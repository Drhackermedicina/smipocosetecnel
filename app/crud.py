from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Optional

from sqlalchemy import and_

from sqlalchemy.orm import Session

from . import models, schemas
from .models import DEFAULT_ALERT_EXPIRATION, InventoryMovementType


def create_supplier(session: Session, supplier: schemas.SupplierCreate) -> models.Supplier:
    conflict = (
        session.query(models.Supplier)
        .filter(models.Supplier.tax_id == supplier.tax_id)
        .first()
    )
    if conflict:
        raise ValueError("Já existe fornecedor com este documento fiscal")

    db_supplier = models.Supplier(**supplier.dict())
    session.add(db_supplier)
    session.flush()
    return db_supplier


def get_supplier(session: Session, supplier_id: int) -> Optional[models.Supplier]:
    return session.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()


def get_suppliers(session: Session) -> List[models.Supplier]:
    return session.query(models.Supplier).all()


def update_supplier(
    session: Session, supplier_id: int, supplier: schemas.SupplierUpdate
) -> models.Supplier:
    db_supplier = get_supplier(session, supplier_id)
    if not db_supplier:
        raise ValueError("Fornecedor não encontrado")

    data = supplier.dict(exclude_unset=True)
    tax_id = data.get("tax_id")
    if tax_id:
        conflict = (
            session.query(models.Supplier)
            .filter(and_(models.Supplier.tax_id == tax_id, models.Supplier.id != supplier_id))
            .first()
        )
        if conflict:
            raise ValueError("Outro fornecedor já utiliza este documento fiscal")

    for field, value in data.items():
        setattr(db_supplier, field, value)

    session.flush()
    return db_supplier


def delete_supplier(session: Session, supplier_id: int) -> None:
    supplier = get_supplier(session, supplier_id)
    if not supplier:
        raise ValueError("Fornecedor não encontrado")
    if supplier.products:
        raise ValueError("Fornecedor possui produtos vinculados")
    session.delete(supplier)
    session.flush()


def create_customer(session: Session, customer: schemas.CustomerCreate) -> models.Customer:
    if customer.tax_id:
        conflict = (
            session.query(models.Customer)
            .filter(models.Customer.tax_id == customer.tax_id)
            .first()
        )
        if conflict:
            raise ValueError("Já existe cliente com este documento fiscal")

    db_customer = models.Customer(**customer.dict())
    session.add(db_customer)
    session.flush()
    return db_customer


def get_customer(session: Session, customer_id: int) -> Optional[models.Customer]:
    return session.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customers(session: Session) -> List[models.Customer]:
    return session.query(models.Customer).all()


def update_customer(
    session: Session, customer_id: int, customer: schemas.CustomerUpdate
) -> models.Customer:
    db_customer = get_customer(session, customer_id)
    if not db_customer:
        raise ValueError("Cliente não encontrado")

    data = customer.dict(exclude_unset=True)
    tax_id = data.get("tax_id")
    if tax_id:
        conflict = (
            session.query(models.Customer)
            .filter(and_(models.Customer.tax_id == tax_id, models.Customer.id != customer_id))
            .first()
        )
        if conflict:
            raise ValueError("Outro cliente já utiliza este documento fiscal")

    for field, value in data.items():
        setattr(db_customer, field, value)

    session.flush()
    return db_customer


def delete_customer(session: Session, customer_id: int) -> None:
    customer = get_customer(session, customer_id)
    if not customer:
        raise ValueError("Cliente não encontrado")
    if customer.invoices:
        raise ValueError("Cliente possui notas vinculadas")
    session.delete(customer)
    session.flush()


def create_product(session: Session, product: schemas.ProductCreate) -> models.Product:
    if product.supplier_id is not None:
        supplier = get_supplier(session, product.supplier_id)
        if not supplier:
            raise ValueError("Fornecedor informado não existe")

    conflict = (
        session.query(models.Product)
        .filter(models.Product.sku == product.sku)
        .first()
    )
    if conflict:
        raise ValueError("Outro produto já utiliza este SKU")

    db_product = models.Product(**product.dict())
    session.add(db_product)
    session.flush()
    return db_product


def get_products(session: Session) -> List[models.Product]:
    return session.query(models.Product).all()


def get_product(session: Session, product_id: int) -> Optional[models.Product]:
    return session.query(models.Product).filter(models.Product.id == product_id).first()


def update_product(
    session: Session, product_id: int, product: schemas.ProductUpdate
) -> models.Product:
    db_product = get_product(session, product_id)
    if not db_product:
        raise ValueError("Produto não encontrado")

    data = product.dict(exclude_unset=True)

    supplier_id = data.get("supplier_id")
    if supplier_id is not None:
        supplier = get_supplier(session, supplier_id)
        if not supplier:
            raise ValueError("Fornecedor informado não existe")

    sku = data.get("sku")
    if sku:
        conflict = (
            session.query(models.Product)
            .filter(and_(models.Product.sku == sku, models.Product.id != product_id))
            .first()
        )
        if conflict:
            raise ValueError("Outro produto já utiliza este SKU")

    for field, value in data.items():
        setattr(db_product, field, value)

    session.flush()
    return db_product


def delete_product(session: Session, product_id: int) -> None:
    product = get_product(session, product_id)
    if not product:
        raise ValueError("Produto não encontrado")
    if product.invoice_items:
        raise ValueError("Produto possui vendas vinculadas")
    if product.inventory_records:
        raise ValueError("Produto possui movimentações de estoque")
    session.delete(product)
    session.flush()


def record_inventory_movement(
    session: Session, movement: schemas.InventoryMovementCreate
) -> models.InventoryMovement:
    db_movement = models.InventoryMovement(**movement.dict())
    session.add(db_movement)

    product = get_product(session, movement.product_id)
    if not product:
        raise ValueError("Produto não encontrado")

    stock_delta = movement.quantity
    if movement.movement_type == InventoryMovementType.EXIT:
        stock_delta *= -1
    elif movement.movement_type == InventoryMovementType.ADJUSTMENT:
        stock_delta = movement.quantity  # already signed

    current_stock = _calculate_stock_level(product)
    projected_stock = current_stock + stock_delta

    if product.max_stock is not None and projected_stock > product.max_stock:
        create_alert(
            session,
            schemas.AlertCreate(
                category="INVENTORY",
                message=(
                    f"Estoque projetado ({projected_stock}) excede o máximo definido "
                    f"({product.max_stock}) para {product.name}"
                ),
            ),
        )

    _evaluate_stock_thresholds(session, product, projected_stock)

    session.flush()
    return db_movement


def _evaluate_stock_thresholds(
    session: Session, product: models.Product, projected_stock: float
) -> None:
    if projected_stock < product.min_stock:
        create_alert(
            session,
            schemas.AlertCreate(
                category="STOCK_LOW",
                message=(
                    f"Estoque baixo para {product.name}: atual {projected_stock}, mínimo {product.min_stock}"
                ),
            ),
        )


def _calculate_stock_level(product: models.Product) -> float:
    stock = 0.0
    for movement in product.inventory_records:
        if movement.movement_type == InventoryMovementType.ENTRY:
            stock += movement.quantity
        elif movement.movement_type == InventoryMovementType.EXIT:
            stock -= movement.quantity
        else:
            stock += movement.quantity
    return stock


def create_invoice(session: Session, invoice: schemas.InvoiceCreate) -> models.Invoice:
    db_invoice = models.Invoice(
        number=invoice.number,
        series=invoice.series,
        customer_id=invoice.customer_id,
        status=invoice.status,
    )
    session.add(db_invoice)
    session.flush()

    total = 0.0
    for item in invoice.items:
        product = get_product(session, item.product_id)
        if not product:
            raise ValueError("Produto não encontrado")

        total_price = item.quantity * item.unit_price
        db_item = models.InvoiceItem(
            invoice_id=db_invoice.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=total_price,
        )
        session.add(db_item)
        total += total_price

        # Automatically deduct from stock
        movement = schemas.InventoryMovementCreate(
            product_id=item.product_id,
            quantity=item.quantity,
            movement_type=InventoryMovementType.EXIT,
            note=f"Saída automática pela nota {invoice.number}",
        )
        record_inventory_movement(session, movement)

    db_invoice.total_value = total
    session.flush()
    return db_invoice


def list_invoices(session: Session) -> List[models.Invoice]:
    return session.query(models.Invoice).all()


def list_inventory_movements(
    session: Session, product_id: int
) -> List[models.InventoryMovement]:
    product = get_product(session, product_id)
    if not product:
        raise ValueError("Produto não encontrado")
    return (
        session.query(models.InventoryMovement)
        .filter(models.InventoryMovement.product_id == product_id)
        .order_by(models.InventoryMovement.created_at.desc())
        .all()
    )


def mark_invoice_as_issued(
    session: Session,
    invoice: models.Invoice,
    fiscal_document_key: str,
    xml_payload: str,
) -> models.Invoice:
    invoice.status = "AUTHORIZED"
    invoice.issued_at = datetime.utcnow()
    invoice.fiscal_document_key = fiscal_document_key
    invoice.xml_payload = xml_payload
    session.add(invoice)
    session.flush()
    return invoice


def create_alert(session: Session, alert: schemas.AlertCreate) -> models.Alert:
    data = alert.dict()
    if not data.get("expires_at"):
        data["expires_at"] = datetime.utcnow() + DEFAULT_ALERT_EXPIRATION
    db_alert = models.Alert(**data)
    session.add(db_alert)
    session.flush()
    return db_alert


def list_alerts(session: Session, include_resolved: bool = False) -> Iterable[models.Alert]:
    query = session.query(models.Alert)
    if not include_resolved:
        query = query.filter(models.Alert.resolved.is_(False))
    return query.order_by(models.Alert.created_at.desc()).all()


def resolve_alert(session: Session, alert_id: int) -> Optional[models.Alert]:
    alert = session.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        return None
    alert.resolved = True
    session.add(alert)
    session.flush()
    return alert
