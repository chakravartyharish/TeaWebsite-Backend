import asyncio
from app.core.mongodb import connect_to_mongo
from app.models.mongo_models import Product, Variant

# Sample product data from your frontend
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
        "story": "Ancient wisdom meets modern wellness in this carefully crafted blend.",
        "ingredients": "Sacred herbs blend with natural adaptogens",
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
        "story": "A timeless classic elevated with premium Ceylon tea leaves.",
        "ingredients": "Ceylon black tea, bergamot oil, cornflower petals",
        "brew_temp_c": 95,
        "brew_time_min": 4,
        "hero_image": "/api/placeholder/600/400",
        "variants": [
            {
                "id": 2,
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
        "story": "From the legendary tea gardens of Hangzhou comes this exquisite green tea.",
        "ingredients": "Premium Chinese green tea leaves",
        "brew_temp_c": 75,
        "brew_time_min": 2,
        "hero_image": "/api/placeholder/600/400",
        "variants": [
            {
                "id": 3,
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
        "story": "Grown at breathtaking altitudes, this tea captures the essence of the Himalayas.",
        "ingredients": "High-altitude Himalayan black tea",
        "brew_temp_c": 95,
        "brew_time_min": 5,
        "hero_image": "/api/placeholder/600/400",
        "variants": [
            {
                "id": 4,
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
        "story": "Let the gentle embrace of chamomile guide you to peaceful dreams.",
        "ingredients": "Organic chamomile flowers, lavender, honey granules",
        "brew_temp_c": 85,
        "brew_time_min": 5,
        "hero_image": "/api/placeholder/600/400",
        "variants": [
            {
                "id": 5,
                "pack_size_g": 100,
                "price_inr": 279,
                "mrp_inr": 319,
                "sku": "CD-100",
                "inventory_qty": 35
            }
        ]
    }
]

async def migrate_products():
    """Migrate products to MongoDB"""
    await connect_to_mongo()
    
    print("Starting product migration...")
    
    # Clear existing products
    await Product.delete_all()
    print("Cleared existing products")
    
    # Insert new products
    for product_data in PRODUCTS_DATA:
        product = Product(**product_data)
        await product.insert()
        print(f"Inserted product: {product.name}")
    
    print(f"Migration completed! Inserted {len(PRODUCTS_DATA)} products.")

if __name__ == "__main__":
    asyncio.run(migrate_products())
