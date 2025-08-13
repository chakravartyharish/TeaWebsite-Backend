from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.admin_guard import admin_guard
from app.models.product import Product, Variant

router = APIRouter(prefix='/admin', tags=['admin'])


@router.post('/products', dependencies=[Depends(admin_guard)])
def create_product(data: dict, db: Session = Depends(get_db)):
    p = Product(**data)
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id}


@router.post('/variants', dependencies=[Depends(admin_guard)])
def create_variant(data: dict, db: Session = Depends(get_db)):
    v = Variant(**data)
    db.add(v)
    db.commit()
    db.refresh(v)
    return {"id": v.id}


