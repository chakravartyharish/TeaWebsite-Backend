from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.mongo_models import Feedback
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

@router.post("/", response_model=dict)
async def create_feedback(feedback_data: dict):
    """Create new feedback"""
    try:
        logger.info(f"Creating feedback from: {feedback_data.get('email')}")
        
        # Validate required fields
        required_fields = ["name", "email", "subject", "message"]
        for field in required_fields:
            if field not in feedback_data or not feedback_data[field]:
                raise HTTPException(status_code=400, detail=f"Field '{field}' is required")
        
        feedback = Feedback(**feedback_data)
        await feedback.insert()
        
        logger.info(f"Successfully created feedback with ID: {feedback.id}")
        
        return {
            "id": str(feedback.id),
            "message": "Feedback submitted successfully",
            "created_at": feedback.created_at.isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating feedback: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[dict])
async def list_feedback(
    status: Optional[str] = Query(None, description="Filter by status"),
    product_id: Optional[str] = Query(None, description="Filter by product ID"),
    limit: int = Query(50, description="Limit number of results"),
    skip: int = Query(0, description="Skip number of results")
):
    """Get all feedback with optional filtering (admin only)"""
    try:
        query = {}
        
        if status:
            query["status"] = status
        if product_id:
            query["product_id"] = product_id
        
        feedback_list = await Feedback.find(query).skip(skip).limit(limit).sort("-created_at").to_list()
        
        result = []
        for feedback in feedback_list:
            feedback_dict = {
                "id": str(feedback.id),
                "name": feedback.name,
                "email": feedback.email,
                "subject": feedback.subject,
                "message": feedback.message,
                "rating": feedback.rating,
                "product_id": feedback.product_id,
                "order_id": feedback.order_id,
                "status": feedback.status,
                "created_at": feedback.created_at.isoformat(),
                "updated_at": feedback.updated_at.isoformat()
            }
            result.append(feedback_dict)
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{feedback_id}", response_model=dict)
async def get_feedback(feedback_id: str):
    """Get a single feedback by ID"""
    try:
        if not ObjectId.is_valid(feedback_id):
            raise HTTPException(status_code=400, detail="Invalid feedback ID format")
        
        feedback = await Feedback.get(ObjectId(feedback_id))
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        
        return {
            "id": str(feedback.id),
            "name": feedback.name,
            "email": feedback.email,
            "subject": feedback.subject,
            "message": feedback.message,
            "rating": feedback.rating,
            "product_id": feedback.product_id,
            "order_id": feedback.order_id,
            "status": feedback.status,
            "created_at": feedback.created_at.isoformat(),
            "updated_at": feedback.updated_at.isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{feedback_id}/status", response_model=dict)
async def update_feedback_status(feedback_id: str, status_data: dict):
    """Update feedback status (admin only)"""
    try:
        if not ObjectId.is_valid(feedback_id):
            raise HTTPException(status_code=400, detail="Invalid feedback ID format")
        
        feedback = await Feedback.get(ObjectId(feedback_id))
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        
        new_status = status_data.get("status")
        if not new_status:
            raise HTTPException(status_code=400, detail="Status is required")
        
        if new_status not in ["pending", "in_progress", "resolved", "closed"]:
            raise HTTPException(status_code=400, detail="Invalid status value")
        
        feedback.status = new_status
        feedback.updated_at = datetime.utcnow()
        await feedback.save()
        
        return {
            "id": str(feedback.id),
            "status": feedback.status,
            "message": "Feedback status updated successfully",
            "updated_at": feedback.updated_at.isoformat()
        }
    except Exception as e:
        logger.error(f"Error updating feedback status: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{feedback_id}", response_model=dict)
async def delete_feedback(feedback_id: str):
    """Delete feedback (admin only)"""
    try:
        if not ObjectId.is_valid(feedback_id):
            raise HTTPException(status_code=400, detail="Invalid feedback ID format")
        
        feedback = await Feedback.get(ObjectId(feedback_id))
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found")
        
        await feedback.delete()
        
        return {"message": "Feedback deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting feedback: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))