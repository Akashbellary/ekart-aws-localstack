from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
async def get_admin_dashboard():
    return {"message": "Admin dashboard endpoint - to be implemented"}

@router.get("/users")
async def get_all_users():
    return {"message": "Get all users - to be implemented", "users": []}

@router.get("/analytics")
async def get_analytics():
    return {"message": "Get analytics - to be implemented"}
