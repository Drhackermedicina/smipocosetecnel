from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .models import InventoryMovementType


class SupplierBase(BaseModel):
    name: str
    tax_id: str = Field(..., description="CNPJ/CPF do fornecedor")
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    tax_id: Optional[str] = Field(None, description="CNPJ/CPF do fornecedor")
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class SupplierRead(SupplierBase):
    id: int

    class Config:
        orm_mode = True


class CustomerBase(BaseModel):
    name: str
    tax_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    tax_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class CustomerRead(CustomerBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    sku: str
    ncm: Optional[str] = Field(None, description="Código NCM do produto")
    unit: str = "UN"
    price: float = 0.0
    min_stock: int = 0
    max_stock: Optional[int] = None
    supplier_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    ncm: Optional[str] = Field(None, description="Código NCM do produto")
    unit: Optional[str] = None
    price: Optional[float] = None
    min_stock: Optional[int] = None
    max_stock: Optional[int] = None
    supplier_id: Optional[int] = None


class ProductRead(ProductBase):
    id: int
    stock_level: float = Field(0, description="Quantidade atual disponível em estoque")

    class Config:
        orm_mode = True


class InventoryMovementBase(BaseModel):
    product_id: int
    quantity: float
    movement_type: InventoryMovementType
    note: Optional[str] = None


class InventoryMovementCreate(InventoryMovementBase):
    pass


class InventoryMovementRead(InventoryMovementBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class InvoiceItemBase(BaseModel):
    product_id: int
    quantity: float
    unit_price: float

    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price


class InvoiceItemCreate(InvoiceItemBase):
    pass


class InvoiceItemRead(InvoiceItemBase):
    id: int
    total_price: float

    class Config:
        orm_mode = True


class InvoiceBase(BaseModel):
    number: str
    series: str
    customer_id: int
    status: str = "DRAFT"
    issued_at: Optional[datetime] = None


class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate]


class InvoiceRead(InvoiceBase):
    id: int
    total_value: float
    fiscal_document_key: Optional[str]
    xml_payload: Optional[str]
    items: List[InvoiceItemRead]

    class Config:
        orm_mode = True


class AlertBase(BaseModel):
    category: str
    message: str
    expires_at: Optional[datetime] = None


class AlertCreate(AlertBase):
    pass


class AlertRead(AlertBase):
    id: int
    resolved: bool
    created_at: datetime

    class Config:
        orm_mode = True
