"""
MongoDB connection module for FastAPI + Beanie.
"""

from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
from pydantic import BaseSettings, Field

# =====================================================
# Settings (tự động load từ file .env)
# =====================================================
class Settings(BaseSettings):
    MONGO_URL: str = Field(..., env="MONGO_URL")
    MONGO_DB: str = Field("class_manager", env="MONGO_DB")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# =====================================================
# Mongo client (global, dùng chung toàn app)
# =====================================================
_motor_client: Optional[AsyncIOMotorClient] = None


async def get_motor_client() -> AsyncIOMotorClient:
    """
    Get or create a global AsyncIOMotorClient.
    """
    global _motor_client
    if _motor_client is None:
        _motor_client = AsyncIOMotorClient(settings.MONGO_URL)
    return _motor_client


# =====================================================
# Beanie init
# =====================================================
async def init_beanie_models(models: List[type[Document]]) -> None:
    """
    Initialize Beanie with given models.
    Call this ONCE in FastAPI startup event.
    """
    client = await get_motor_client()
    db = client[settings.MONGO_DB]
    await init_beanie(database=db, document_models=models)


# =====================================================
# Close client on shutdown
# =====================================================
async def close_motor_client() -> None:
    """
    Properly close MongoDB client on shutdown.
    """
    global _motor_client
    if _motor_client is not None:
        _motor_client.close()
        _motor_client = None
