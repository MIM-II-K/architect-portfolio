from sqlalchemy import Column, Integer, String, Boolean, Text
from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_order=True, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    cover_image = Column(String, nullable=True)  # Stores Supabase public URL
    category = Column(String, nullable=True)
    year = Column(Integer, default=2024)
    published = Column(Boolean, default=True)