from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.user_profile import router as user_profile_router
from app.api.v1.recommendations import router as recommendations_router

api_router = APIRouter()

@api_router.get("/health")
def health_check():
    return {"status": "ok"}

api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(jobs_router, tags=["Jobs"])
api_router.include_router(user_profile_router, tags=["User Profile"])
api_router.include_router(
    recommendations_router,
    tags=["Recommendations"],
)
