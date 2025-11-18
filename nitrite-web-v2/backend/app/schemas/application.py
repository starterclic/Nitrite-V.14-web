from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ApplicationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=100)
    winget_id: Optional[str] = Field(None, max_length=255)
    download_url: Optional[str] = Field(None, max_length=500)
    install_args: Optional[str] = Field(None, max_length=255)
    essential: bool = False
    admin_required: bool = True
    icon_url: Optional[str] = None
    website: Optional[str] = None
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    winget_id: Optional[str] = None
    download_url: Optional[str] = None
    install_args: Optional[str] = None
    essential: Optional[bool] = None
    admin_required: Optional[bool] = None
    icon_url: Optional[str] = None
    website: Optional[str] = None
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Application(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ApplicationList(BaseModel):
    applications: list[Application]
    total: int
    page: int
    page_size: int
