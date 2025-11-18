from sqlalchemy import Column, Integer, String, Boolean, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100), nullable=False, index=True)
    winget_id = Column(String(255), unique=True, index=True)
    download_url = Column(String(500))
    install_args = Column(String(255))
    essential = Column(Boolean, default=False)
    admin_required = Column(Boolean, default=True)
    icon_url = Column(String(500))
    website = Column(String(500))
    version = Column(String(50))
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Application {self.name}>"
