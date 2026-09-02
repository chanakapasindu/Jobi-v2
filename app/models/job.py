from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db.session import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # who created the job (user id)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
