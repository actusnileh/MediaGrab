from sqlalchemy import Column, Date, ForeignKey, Integer, String
from database.database import Base


class Videos(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String, nullable=False)
    download_at = Column(Date, nullable=False)
