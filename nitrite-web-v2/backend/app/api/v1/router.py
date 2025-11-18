from fastapi import APIRouter
from app.api.v1.endpoints import applications, tools, profiles, system

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    applications.router,
    prefix="/applications",
    tags=["Applications"]
)

api_router.include_router(
    tools.router,
    prefix="/tools",
    tags=["Outils Système"]
)

api_router.include_router(
    profiles.router,
    prefix="/profiles",
    tags=["Profils"]
)

api_router.include_router(
    system.router,
    prefix="/system",
    tags=["Système"]
)
