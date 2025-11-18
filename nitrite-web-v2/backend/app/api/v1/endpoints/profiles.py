from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.base import get_db
from app.db.models.profile import Profile

router = APIRouter()


@router.get("/")
async def get_profiles(db: AsyncSession = Depends(get_db)):
    """
    Récupérer tous les profils prédéfinis
    """
    query = select(Profile)
    result = await db.execute(query)
    profiles = result.scalars().all()

    return {
        "profiles": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "icon": p.icon,
                "applications": p.applications,
                "tools": p.tools,
            }
            for p in profiles
        ]
    }


@router.get("/{profile_id}")
async def get_profile(
    profile_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Récupérer un profil par ID
    """
    query = select(Profile).where(Profile.id == profile_id)
    result = await db.execute(query)
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "id": profile.id,
        "name": profile.name,
        "description": profile.description,
        "icon": profile.icon,
        "applications": profile.applications,
        "tools": profile.tools,
    }


@router.post("/{profile_id}/install")
async def install_profile(
    profile_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Installer toutes les applications d'un profil
    """
    query = select(Profile).where(Profile.id == profile_id)
    result = await db.execute(query)
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # TODO: Launch bulk installation Celery task
    # For now, return mock response

    return {
        "status": "started",
        "profile_id": profile_id,
        "profile_name": profile.name,
        "app_count": len(profile.applications) if profile.applications else 0,
        "message": "Profile installation started (not implemented yet)"
    }
