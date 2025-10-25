from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import os

from config.database import init_db
from api.auth.routes import router as auth_router
from api.products.routes import router as products_router
from api.orders.routes import router as orders_router
from api.cart.routes import router as cart_router
from api.sellers.routes import router as sellers_router
from api.admin.routes import router as admin_router
from api.payments.routes import router as payments_router

# Initialize FastAPI app
app = FastAPI(
    title="EKart Store API",
    description="Complete E-Commerce Backend API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(products_router, prefix="/api/products", tags=["Products"])
app.include_router(orders_router, prefix="/api/orders", tags=["Orders"])
app.include_router(cart_router, prefix="/api/cart", tags=["Cart"])
app.include_router(sellers_router, prefix="/api/sellers", tags=["Sellers"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
app.include_router(payments_router, tags=["Payments"])

@app.on_event("startup")
async def startup_event():
    """Initialize database connections and AWS services"""
    await init_db()

@app.get("/")
async def root():
    return {"message": "EKart Store API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ekart-api"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("ENV") == "development" else False
    )
