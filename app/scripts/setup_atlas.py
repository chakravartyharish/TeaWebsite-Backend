"""
MongoDB Atlas Setup and Migration Script
This script connects to MongoDB Atlas and populates it with initial tea product data.
"""

import asyncio
import os
from app.core.mongodb import connect_to_mongo
from app.models.mongo_models import Product, Category

# Enhanced product data for MongoDB Atlas
CATEGORIES_DATA = [
    {
        "name": "Wellness Blend",
        "description": "Therapeutic teas crafted for health and wellness",
        "slug": "wellness-blend"
    },
    {
        "name": "Black Tea",
        "description": "Rich and robust black tea varieties",
        "slug": "black-tea"
    },
    {
        "name": "Green Tea",
        "description": "Fresh and antioxidant-rich green teas",
        "slug": "green-tea"
    },
    {
        "name": "Herbal Tea",
        "description": "Caffeine-free herbal blends for relaxation",
        "slug": "herbal-tea"
    }
]

PRODUCTS_DATA = [
    {
        "name": "A-ZEN Calm Blend",
        "description": "Hand crafted with 5 sacred herbs. Ancient wisdom for modern mind. Instant tea/latte mix for calm & focused mind + radiant skin.",
        "price": 249,
        "original_price": 299,
        "image": "/api/placeholder/300/300",
        "category": "Wellness Blend",
        "benefits": ["Reduces anxiety", "Improves focus", "Radiant skin", "Natural ingredients"],
        "in_stock": True,
        "rating": 4.8,
        "reviews": 127,
        "slug": "a-zen-calm-blend",
        "story": "Ancient wisdom meets modern wellness in this carefully crafted blend of sacred herbs.",
        "ingredients": "Sacred herbs blend with natural adaptogens including ashwagandha, brahmi, and tulsi",
        "brew_temp_c": 80,
        "brew_time_min": 3,
        "hero_image": "/api/placeholder/600/400",
        "variants": [
            {
                "id": 1,
                "pack_size_g": 100,
                "price_inr": 249,
                "mrp_inr": 299,
                "sku": "AZN-100",
                "inventory_qty": 50
            },
            {
                "id": 2,
                "pack_size_g": 250,
                "price_inr": 599,
                "mrp_inr": 699,
                "sku": "AZN-250",
                "inventory_qty": 25
            }
        ]
    },
    {
        "name": "Earl Grey Supreme",
        "description": "Premium Ceylon black tea infused with bergamot oil and cornflower petals. A classic with a luxurious twist.",
        "price": 399,
        "original_price": 449,
        "image": "/api/placeholder/300/300",
        "category": "Black Tea",
        "benefits": ["Rich antioxidants", "Energy boost", "Classic flavor", "Premium quality"],
        "in_stock": True,
        "rating": 4.7,
        "reviews": 89,
        "slug": "earl-grey-supreme",
        "story": "A timeless classic elevated with premium Ceylon tea leaves and natural bergamot.",
        "ingredients": "Ceylon black tea, natural bergamot oil, cornflower petals",
        "brew_temp_c": 95,
        "brew_time_min": 4,
        "hero_image": "/api/placeholder/600/400",
        "variants": [
            {
                "id": 3,
                "pack_size_g": 100,
                "price_inr": 399,
                "mrp_inr": 449,
                "sku": "EGS-100",
                "inventory_qty": 30
            }
        ]
    },
    {
        "name": "Dragon Well Green",
        "description": "Delicate Chinese green tea with a nutty flavor. Hand-picked from the hills of Hangzhou.",
        "price": 329,
        "original_price": 379,
        "image": "/api/placeholder/300/300",
        "category": "Green Tea",
        "benefits": ["High antioxidants", "Metabolism boost", "Mental clarity", "Traditional taste"],
        "in_stock": True,
        "rating": 4.6,
        "reviews": 156,
        "slug": "dragon-well-green",
        "story": "From the legendary tea gardens of Hangzhou comes this exquisite green tea with centuries of tradition.",
        "ingredients": "Premium Chinese green tea leaves (Longjing variety)",
        "brew_temp_c": 75,
        "brew_time_min": 2,
        "hero_image": "/api/placeholder/600/400",
        "variants": [
            {
                "id": 4,
                "pack_size_g": 100,
                "price_inr": 329,
                "mrp_inr": 379,
                "sku": "DWG-100",
                "inventory_qty": 40
            }
        ]
    },
    {
        "name": "Himalayan Gold",
        "description": "High-altitude black tea from the Himalayas. Bold flavor with floral notes and golden liquor.",
        "price": 459,
        "original_price": 509,
        "image": "/api/placeholder/300/300",
        "category": "Black Tea",
        "benefits": ["Premium quality", "Bold flavor", "High altitude", "Floral notes"],
        "in_stock": True,
        "rating": 4.9,
        "reviews": 203,
        "slug": "himalayan-gold",
        "story": "Grown at breathtaking altitudes in the Himalayas, this tea captures the pure essence of mountain terroir.",
        "ingredients": "High-altitude Himalayan black tea leaves",
        "brew_temp_c": 95,
        "brew_time_min": 5,
        "hero_image": "/api/placeholder/600/400",
        "variants": [
            {
                "id": 5,
                "pack_size_g": 100,
                "price_inr": 459,
                "mrp_inr": 509,
                "sku": "HG-100",
                "inventory_qty": 25
            }
        ]
    },
    {
        "name": "Chamomile Dreams",
        "description": "Soothing herbal blend perfect for bedtime. Naturally caffeine-free with calming properties.",
        "price": 279,
        "original_price": 319,
        "image": "/api/placeholder/300/300",
        "category": "Herbal Tea",
        "benefits": ["Caffeine-free", "Promotes sleep", "Calming effect", "Natural herbs"],
        "in_stock": True,
        "rating": 4.5,
        "reviews": 94,
        "slug": "chamomile-dreams",
        "story": "Let the gentle embrace of chamomile and lavender guide you to peaceful, restorative sleep.",
        "ingredients": "Organic chamomile flowers, lavender, honey granules, lemon balm",
        "brew_temp_c": 85,
        "brew_time_min": 5,
        "hero_image": "/api/placeholder/600/400",
        "variants": [
            {
                "id": 6,
                "pack_size_g": 100,
                "price_inr": 279,
                "mrp_inr": 319,
                "sku": "CD-100",
                "inventory_qty": 35
            }
        ]
    }
]

async def setup_atlas_database():
    """Setup MongoDB Atlas with initial data"""
    try:
        print("🚀 Connecting to MongoDB Atlas...")
        await connect_to_mongo()
        print("✅ Connected to MongoDB Atlas successfully!")
        
        # Clear existing data
        print("🧹 Clearing existing data...")
        await Product.delete_all()
        await Category.delete_all()
        print("✅ Cleared existing data")
        
        # Insert categories
        print("📁 Creating categories...")
        for category_data in CATEGORIES_DATA:
            category = Category(**category_data)
            await category.insert()
            print(f"  ✅ Created category: {category.name}")
        
        # Insert products
        print("🍃 Creating products...")
        for product_data in PRODUCTS_DATA:
            product = Product(**product_data)
            await product.insert()
            print(f"  ✅ Created product: {product.name}")
        
        print(f"\n🎉 Atlas setup completed successfully!")
        print(f"📊 Created {len(CATEGORIES_DATA)} categories and {len(PRODUCTS_DATA)} products")
        print(f"🌐 Your MongoDB Atlas database is ready!")
        
        # Verify data
        product_count = await Product.count()
        category_count = await Category.count()
        print(f"\n📈 Verification:")
        print(f"  Products in database: {product_count}")
        print(f"  Categories in database: {category_count}")
        
    except Exception as e:
        print(f"❌ Error setting up Atlas database: {str(e)}")
        print("💡 Make sure your MongoDB Atlas connection string is correct in .env file")
        print("💡 Check that your IP address is whitelisted in MongoDB Atlas")
        raise e

if __name__ == "__main__":
    print("🍃 MongoDB Atlas Setup for Tea Store")
    print("=" * 50)
    asyncio.run(setup_atlas_database())
