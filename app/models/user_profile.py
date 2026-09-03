from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from app.db.session import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
        index=True,
    )

    skills = Column(JSON, nullable=True)
    education = Column(JSON, nullable=True)
    experience = Column(JSON, nullable=True)
    preferred_roles = Column(JSON, nullable=True)
    preferred_locations = Column(JSON, nullable=True)

    employment_type = Column(String(50), nullable=True)
    experience_level = Column(String(50), nullable=True)