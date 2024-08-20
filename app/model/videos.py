from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Videos(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String, nullable=False)
    download_at = Column(Date, nullable=False)

    users = relationship("Users", back_populates="videos")

    def __str__(self):
        return f"Видео #{self.id}"
