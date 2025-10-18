from __future__ import annotations

from datetime import datetime, timedelta

from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    tax_id = Column(String(32), unique=True, nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(32), nullable=True)
    address = Column(Text, nullable=True)

    products = relationship("Product", back_populates="supplier")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    tax_id = Column(String(32), unique=True, nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(32), nullable=True)
    address = Column(Text, nullable=True)

    invoices = relationship("Invoice", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(64), unique=True, nullable=False)
    ncm = Column(String(16), nullable=True)
    unit = Column(String(16), nullable=False, default="UN")
    price = Column(Float, nullable=False, default=0.0)
    min_stock = Column(Integer, nullable=False, default=0)
    max_stock = Column(Integer, nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)

    supplier = relationship("Supplier", back_populates="products")
    inventory_records = relationship("InventoryMovement", back_populates="product")
    invoice_items = relationship("InvoiceItem", back_populates="product")

    @property
    def stock_level(self) -> float:
        """Calculate the current stock level based on movements."""
        total = 0.0
        for movement in self.inventory_records:
            if movement.movement_type == InventoryMovementType.ENTRY:
                total += movement.quantity
            elif movement.movement_type == InventoryMovementType.EXIT:
                total -= movement.quantity
            else:
                total += movement.quantity
        return total


class InventoryMovementType(str, PyEnum):
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    ADJUSTMENT = "ADJUSTMENT"


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    movement_type = Column(Enum(InventoryMovementType), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Product", back_populates="inventory_records")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(64), unique=True, nullable=False)
    series = Column(String(16), nullable=False)
    status = Column(String(32), nullable=False, default="DRAFT")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    total_value = Column(Float, nullable=False, default=0.0)
    issued_at = Column(DateTime, nullable=True)
    fiscal_document_key = Column(String(44), nullable=True)
    xml_payload = Column(Text, nullable=True)

    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product", back_populates="invoice_items")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(64), nullable=False)
    message = Column(Text, nullable=False)
    resolved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)

    @property
    def is_expired(self) -> bool:
        return bool(self.expires_at and datetime.utcnow() > self.expires_at)


DEFAULT_ALERT_EXPIRATION = timedelta(days=7)
