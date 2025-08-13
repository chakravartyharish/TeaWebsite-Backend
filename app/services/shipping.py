import os

SHIPROCKET_TOKEN = os.getenv("SHIPROCKET_TOKEN")


async def create_shipment(order_id: int, payload: dict):
    # TODO: integrate actual Shiprocket API
    return {"tracking_id": "SR123"}


