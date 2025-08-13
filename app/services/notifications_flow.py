from app.services.notify import send_whatsapp


async def notify_order_placed(phone: str, order_id: int, amount_inr: int):
    await send_whatsapp(phone, template="order_placed", variables=[str(order_id), f"₹{amount_inr}"])


async def notify_order_shipped(phone: str, order_id: int, tracking: str):
    await send_whatsapp(phone, template="order_shipped", variables=[str(order_id), tracking])


async def notify_order_delivered(phone: str, order_id: int):
    await send_whatsapp(phone, template="order_delivered", variables=[str(order_id)])


