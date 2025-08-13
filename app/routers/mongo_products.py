from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.mongo_models import Product, Category
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=List[dict])
async def list_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    in_stock: Optional[bool] = Query(None, description="Filter by stock status"),
    limit: int = Query(50, description="Limit number of results"),
    skip: int = Query(0, description="Skip number of results")
):
    """Get all products with optional filtering"""
    try:
        logger.info(f"Starting list_products request with category={category}, in_stock={in_stock}")
        
        query = {}
        
        if category:
            query["category"] = category
        if in_stock is not None:
            query["in_stock"] = in_stock
        
        logger.info(f"MongoDB query: {query}")
        
        # Add timeout and better error handling
        products = await Product.find(query).skip(skip).limit(limit).to_list()
        
        logger.info(f"Successfully retrieved {len(products)} products from MongoDB")
        
        result = []
        for product in products:
            try:
                product_dict = {
                    "id": str(product.id),
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "original_price": product.original_price,
                    "image": product.image,
                    "category": product.category,
                    "benefits": product.benefits,
                    "in_stock": product.in_stock,
                    "rating": product.rating,
                    "reviews": product.reviews,
                    "slug": product.slug
                }
                result.append(product_dict)
            except Exception as e:
                logger.error(f"Error processing product {product.id}: {str(e)}")
                continue
        
        logger.info(f"Successfully processed {len(result)} products for response")
        return result
        
    except Exception as e:
        logger.error(f"Error in list_products: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve products: {str(e)}")

@router.get("/{product_id}", response_model=dict)
async def get_product(product_id: str):
    """Get a single product by ID"""
    try:
        if ObjectId.is_valid(product_id):
            product = await Product.get(ObjectId(product_id))
        else:
            # Try to find by slug if not a valid ObjectId
            product = await Product.find_one(Product.slug == product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "original_price": product.original_price,
            "image": product.image,
            "category": product.category,
            "benefits": product.benefits,
            "in_stock": product.in_stock,
            "rating": product.rating,
            "reviews": product.reviews,
            "slug": product.slug,
            "story": product.story,
            "ingredients": product.ingredients,
            "brew_temp_c": product.brew_temp_c,
            "brew_time_min": product.brew_time_min,
            "hero_image": product.hero_image,
            "variants": product.variants
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/category/{category_name}", response_model=List[dict])
async def get_products_by_category(category_name: str):
    """Get all products in a specific category"""
    products = await Product.find(Product.category == category_name).to_list()
    
    return [
        {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "original_price": product.original_price,
            "image": product.image,
            "category": product.category,
            "benefits": product.benefits,
            "in_stock": product.in_stock,
            "rating": product.rating,
            "reviews": product.reviews,
            "slug": product.slug
        }
        for product in products
    ]

@router.post("/", response_model=dict)
async def create_product(product_data: dict):
    """Create a new product"""
    try:
        product = Product(**product_data)
        await product.insert()
        
        return {
            "id": str(product.id),
            "message": "Product created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{product_id}", response_model=dict)
async def update_product(product_id: str, product_data: dict):
    """Update an existing product"""
    try:
        product = await Product.get(ObjectId(product_id))
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Update fields
        for key, value in product_data.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        await product.save()
        
        return {
            "id": str(product.id),
            "message": "Product updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    """Delete a product"""
    try:
        product = await Product.get(ObjectId(product_id))
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        await product.delete()
        
        return {"message": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
