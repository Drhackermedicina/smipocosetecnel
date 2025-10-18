from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/partners", tags=["partners"])


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/suppliers", response_model=schemas.SupplierRead, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier: schemas.SupplierCreate, session: Session = Depends(get_session)):
    try:
        return crud.create_supplier(session, supplier)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/suppliers", response_model=list[schemas.SupplierRead])
def list_suppliers(session: Session = Depends(get_session)):
    return crud.get_suppliers(session)


@router.get("/suppliers/{supplier_id}", response_model=schemas.SupplierRead)
def retrieve_supplier(supplier_id: int, session: Session = Depends(get_session)):
    supplier = crud.get_supplier(session, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return supplier


@router.put("/suppliers/{supplier_id}", response_model=schemas.SupplierRead)
def update_supplier(
    supplier_id: int,
    supplier: schemas.SupplierUpdate,
    session: Session = Depends(get_session),
):
    try:
        return crud.update_supplier(session, supplier_id, supplier)
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "não encontrado" in detail else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=detail) from exc


@router.delete("/suppliers/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, session: Session = Depends(get_session)):
    try:
        crud.delete_supplier(session, supplier_id)
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "não encontrado" in detail else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=detail) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/customers", response_model=schemas.CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate, session: Session = Depends(get_session)):
    try:
        return crud.create_customer(session, customer)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/customers", response_model=list[schemas.CustomerRead])
def list_customers(session: Session = Depends(get_session)):
    return crud.get_customers(session)


@router.get("/customers/{customer_id}", response_model=schemas.CustomerRead)
def retrieve_customer(customer_id: int, session: Session = Depends(get_session)):
    customer = crud.get_customer(session, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return customer


@router.put("/customers/{customer_id}", response_model=schemas.CustomerRead)
def update_customer(
    customer_id: int,
    customer: schemas.CustomerUpdate,
    session: Session = Depends(get_session),
):
    try:
        return crud.update_customer(session, customer_id, customer)
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "não encontrado" in detail else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=detail) from exc


@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, session: Session = Depends(get_session)):
    try:
        crud.delete_customer(session, customer_id)
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "não encontrado" in detail else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=detail) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
