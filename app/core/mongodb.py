from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.mongo_models import Product, Category
import os
import asyncio
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

mongodb = MongoDB()

async def connect_to_mongo():
    """Create database connection with enhanced error handling"""
    try:
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        mongodb_db = os.getenv("MONGODB_DB", "teawebsite")
        
        logger.info(f"Connecting to MongoDB at: {mongodb_url}")
        logger.info(f"Database: {mongodb_db}")
        
        # Create client with timeout settings
        mongodb.client = AsyncIOMotorClient(
            mongodb_url,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
        )
        
        # Test the connection
        await mongodb.client.admin.command('ping')
        logger.info("Successfully pinged MongoDB!")
        
        mongodb.database = mongodb.client[mongodb_db]
        
        # Initialize beanie with the Product model
        await init_beanie(
            database=mongodb.database,
            document_models=[Product, Category]
        )
        
        # Test that products collection is accessible
        product_count = await Product.count()
        logger.info(f"Connected to MongoDB! Found {product_count} products in database.")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        logger.error("Please check your MONGODB_URL and MONGODB_DB environment variables")
        raise e

async def close_mongo_connection():
    """Close database connection"""
    try:
        if mongodb.client:
            mongodb.client.close()
            logger.info("MongoDB connection closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {str(e)}")

def get_database():
    return mongodb.database
