from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    section = Column(String(100), nullable=False, index=True)
    command = Column(Text)
    requires_admin = Column(Integer, default=1)  # 0=no, 1=yes
    icon = Column(String(50))
    category = Column(String(100))
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Tool {self.name}>"
