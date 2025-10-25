from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
async def get_seller_dashboard():
    return {"message": "Seller dashboard endpoint - to be implemented"}

@router.get("/products")
async def get_seller_products():
    return {"message": "Get seller products - to be implemented", "products": []}

@router.get("/orders")
async def get_seller_orders():
    return {"message": "Get seller orders - to be implemented", "orders": []}
