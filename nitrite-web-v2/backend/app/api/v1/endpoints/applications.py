from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from app.db.base import get_db
from app.db.models.application import Application
from app.schemas.application import (
    Application as ApplicationSchema,
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationList,
)

router = APIRouter()


@router.get("/", response_model=ApplicationList)
async def get_applications(
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    Récupérer la liste des applications avec filtres et pagination
    """
    # Build query
    query = select(Application)

    # Apply filters
    if category:
        query = query.where(Application.category == category)

    if search:
        query = query.where(
            Application.name.ilike(f"%{search}%") |
            Application.description.ilike(f"%{search}%")
        )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Apply pagination
    query = query.offset((page - 1) * page_size).limit(page_size)

    # Execute query
    result = await db.execute(query)
    applications = result.scalars().all()

    return ApplicationList(
        applications=applications,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    """
    Récupérer toutes les catégories uniques
    """
    query = select(Application.category).distinct()
    result = await db.execute(query)
    categories = result.scalars().all()

    return {"categories": sorted(categories)}


@router.get("/{app_id}", response_model=ApplicationSchema)
async def get_application(
    app_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Récupérer une application par ID
    """
    query = select(Application).where(Application.id == app_id)
    result = await db.execute(query)
    app = result.scalar_one_or_none()

    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    return app


@router.post("/", response_model=ApplicationSchema)
async def create_application(
    application: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Créer une nouvelle application
    """
    db_app = Application(**application.dict())
    db.add(db_app)
    await db.commit()
    await db.refresh(db_app)

    return db_app


@router.post("/{app_id}/install")
async def install_application(
    app_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Lancer l'installation d'une application
    """
    # Get application
    query = select(Application).where(Application.id == app_id)
    result = await db.execute(query)
    app = result.scalar_one_or_none()

    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    # TODO: Launch Celery task for installation
    # For now, return mock response

    return {
        "status": "started",
        "app_id": app_id,
        "app_name": app.name,
        "message": "Installation started (not implemented yet)"
    }
