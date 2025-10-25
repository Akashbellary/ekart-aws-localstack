from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import List, Optional
import uuid
from datetime import datetime

from models.product import Product, ProductCreate, ProductUpdate, ProductFilter, ProductSearchQuery
from models.user import UserProfile
from services.product_service import ProductService
from services.auth_service import get_current_user
from services.file_service import upload_product_image

router = APIRouter()
product_service = ProductService()

@router.get("/", response_model=List[Product])
async def get_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    brand: Optional[str] = None,
    seller_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Get products with optional filtering and pagination"""
    filters = ProductFilter(
        category=category,
        min_price=min_price,
        max_price=max_price,
        brand=brand,
        seller_id=seller_id
    )
    return await product_service.get_products(filters, page, per_page)

@router.get("/search", response_model=List[Product])
async def search_products(
    q: str = Query(..., min_length=1),
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "relevance",
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Search products by query with filters"""
    search_query = ProductSearchQuery(
        query=q,
        filters=ProductFilter(
            category=category,
            min_price=min_price,
            max_price=max_price
        ),
        sort_by=sort_by,
        page=page,
        per_page=per_page
    )
    return await product_service.search_products(search_query)

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=Product)
async def create_product(
    product_data: ProductCreate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Create a new product (sellers only)"""
    if current_user.user_type != "seller" or not current_user.seller_verified:
        raise HTTPException(status_code=403, detail="Only verified sellers can create products")
    
    product_id = str(uuid.uuid4())
    return await product_service.create_product(product_id, current_user.user_id, product_data)

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    current_user: UserProfile = Depends(get_current_user)
):
    """Update a product (owner only)"""
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.seller_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only update your own products")
    
    return await product_service.update_product(product_id, product_data)

@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    current_user: UserProfile = Depends(get_current_user)
):
    """Delete a product (owner only)"""
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.seller_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own products")
    
    await product_service.delete_product(product_id)
    return {"message": "Product deleted successfully"}

@router.post("/{product_id}/images")
async def upload_product_images(
    product_id: str,
    files: List[UploadFile] = File(...),
    current_user: UserProfile = Depends(get_current_user)
):
    """Upload images for a product"""
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.seller_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only upload images for your own products")
    
    uploaded_images = []
    for file in files:
        if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(status_code=400, detail="Only JPEG, PNG, and WebP images are allowed")
        
        image_url = await upload_product_image(product_id, file)
        uploaded_images.append(image_url)
    
    await product_service.add_product_images(product_id, uploaded_images)
    return {"message": f"Uploaded {len(uploaded_images)} images", "urls": uploaded_images}

@router.get("/categories/")
async def get_categories():
    """Get all available product categories"""
    return await product_service.get_categories()
