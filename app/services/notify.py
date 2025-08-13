import httpx, os

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")


async def send_whatsapp(to_phone: str, template: str, variables: list[str] = []):
    url = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "template",
        "template": {
            "name": template,
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": v} for v in variables
                    ],
                }
            ],
        },
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=data, headers=headers)
        r.raise_for_status()
        return r.json()


