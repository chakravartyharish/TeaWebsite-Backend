from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from beanie import Document
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/leads", tags=["leads"])

class Lead(Document):
    phone: Optional[str] = None
    email: Optional[str] = None
    source: str = "popup"
    marketing_optin: bool = False
    whatsapp_optin: bool = False
    created_at: datetime = datetime.utcnow()
    
    class Settings:
        name = "leads"

class LeadIn(BaseModel):
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    source: str = "popup"
    marketing_optin: bool = False
    whatsapp_optin: bool = False

@router.post("/")
async def create_or_update_lead(data: LeadIn):
    """Create or update a lead in MongoDB"""
    try:
        # Try to find existing lead
        existing = None
        if data.phone:
            existing = await Lead.find_one(Lead.phone == data.phone)
        elif data.email:
            existing = await Lead.find_one(Lead.email == data.email)
        
        if existing:
            # Update existing lead
            for key, value in data.dict(exclude_unset=True).items():
                setattr(existing, key, value)
            await existing.save()
            return {"id": str(existing.id), "message": "Lead updated"}
        else:
            # Create new lead
            lead = Lead(**data.dict())
            await lead.insert()
            return {"id": str(lead.id), "message": "Lead created"}
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def list_leads():
    """List all leads"""
    try:
        leads = await Lead.find_all().to_list()
        return [
            {
                "id": str(lead.id),
                "phone": lead.phone,
                "email": lead.email,
                "source": lead.source,
                "created_at": lead.created_at
            }
            for lead in leads
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
