from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/products", tags=["products"])


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/", response_model=schemas.ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, session: Session = Depends(get_session)):
    try:
        return crud.create_product(session, product)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/", response_model=list[schemas.ProductRead])
def list_products(session: Session = Depends(get_session)):
    return crud.get_products(session)


@router.get("/{product_id}", response_model=schemas.ProductRead)
def retrieve_product(product_id: int, session: Session = Depends(get_session)):
    product = crud.get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@router.put("/{product_id}", response_model=schemas.ProductRead)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    session: Session = Depends(get_session),
):
    try:
        return crud.update_product(session, product_id, product)
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "não encontrado" in detail else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=detail) from exc


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    try:
        crud.delete_product(session, product_id)
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "não encontrado" in detail else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=detail) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{product_id}/inventory", response_model=list[schemas.InventoryMovementRead]
)
def list_inventory_movements(product_id: int, session: Session = Depends(get_session)):
    try:
        return crud.list_inventory_movements(session, product_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{product_id}/inventory", response_model=schemas.InventoryMovementRead)
def record_inventory(
    product_id: int,
    movement: schemas.InventoryMovementCreate,
    session: Session = Depends(get_session),
):
    if movement.product_id != product_id:
        raise HTTPException(status_code=400, detail="Produto inconsistente")
    try:
        return crud.record_inventory_movement(session, movement)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
