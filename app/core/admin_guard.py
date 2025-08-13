import os
from fastapi import Header, HTTPException


def admin_guard(x_admin_key: str | None = Header(None)):
    if x_admin_key != os.getenv('ADMIN_API_KEY'):
        raise HTTPException(401, 'Unauthorized')


