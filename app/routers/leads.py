from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
# MongoDB-only - SQLAlchemy removed
from app.models.lead import Lead

router = APIRouter(prefix="/leads", tags=["leads"])


class LeadIn(BaseModel):
    phone: str | None = None
    email: EmailStr | None = None
    source: str = "popup"
    marketing_optin: bool = False
    whatsapp_optin: bool = False


def upsert_lead(payload: LeadIn):
    q = db.query(Lead)
    if payload.phone:
        q = q.filter(Lead.phone == payload.phone)
    elif payload.email:
        q = q.filter(Lead.email == payload.email)
    existing = q.first()
    if existing:
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(existing, k, v)
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    new = Lead(**payload.model_dump())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.post("")
def create_lead(lead: LeadIn, db: Session = Depends(get_db)):
    lead = upsert_lead(db, lead)
    return {"id": lead.id}
