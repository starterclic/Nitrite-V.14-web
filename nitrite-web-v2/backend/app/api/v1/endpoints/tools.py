from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.db.base import get_db
from app.db.models.tool import Tool

router = APIRouter()


@router.get("/")
async def get_tools(
    section: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Récupérer la liste des outils système avec filtre par section
    """
    query = select(Tool)

    if section:
        query = query.where(Tool.section == section)

    result = await db.execute(query)
    tools = result.scalars().all()

    # Group by section
    tools_by_section = {}
    for tool in tools:
        if tool.section not in tools_by_section:
            tools_by_section[tool.section] = []
        tools_by_section[tool.section].append({
            "id": tool.id,
            "name": tool.name,
            "description": tool.description,
            "command": tool.command,
            "requires_admin": tool.requires_admin,
            "icon": tool.icon,
        })

    return {"tools": tools_by_section}


@router.get("/sections")
async def get_sections(db: AsyncSession = Depends(get_db)):
    """
    Récupérer toutes les sections uniques
    """
    query = select(Tool.section).distinct()
    result = await db.execute(query)
    sections = result.scalars().all()

    return {"sections": sorted(sections)}


@router.post("/{tool_id}/execute")
async def execute_tool(
    tool_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Exécuter un outil système
    """
    query = select(Tool).where(Tool.id == tool_id)
    result = await db.execute(query)
    tool = result.scalar_one_or_none()

    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    # TODO: Execute command with proper elevation
    # For now, return mock response

    return {
        "status": "executed",
        "tool_id": tool_id,
        "tool_name": tool.name,
        "command": tool.command,
        "message": "Tool executed (not implemented yet)"
    }
