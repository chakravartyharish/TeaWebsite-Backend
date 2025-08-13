from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatIn(BaseModel):
    message: str
    context: dict | None = None


@router.post("/chat")
async def chat(msg: ChatIn):
    # TODO: plug LLM provider
    return {"reply": "Hi! Tell me how you like your tea—floral, bold, or herbal?"}


