from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+psycopg2://teastore:teastore@db:5432/teastore"
    REDIS_URL: str = "redis://redis:6379/0"
    SECRET_KEY: str = "change-me"

    # OTP/Comms
    MSG91_API_KEY: str | None = None
    TWILIO_SID: str | None = None
    TWILIO_TOKEN: str | None = None
    WHATSAPP_TOKEN: str | None = None
    WHATSAPP_PHONE_ID: str | None = None

    # Payments
    RAZORPAY_KEY_ID: str | None = None
    RAZORPAY_KEY_SECRET: str | None = None

    # Shipping
    SHIPROCKET_TOKEN: str | None = None

    # Admin
    ADMIN_API_KEY: str | None = None

    # Clerk (optional, for verifying session JWTs later)
    CLERK_JWKS_URL: str | None = None


settings = Settings()

