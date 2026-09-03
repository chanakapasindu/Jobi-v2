from pydantic import BaseModel, Field


class UserProfileCreate(BaseModel):
    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    preferred_roles: list[str] = Field(default_factory=list)
    preferred_locations: list[str] = Field(default_factory=list)
    employment_type: str | None = Field(default=None, max_length=50)
    experience_level: str | None = Field(default=None, max_length=50)


class UserProfileOut(UserProfileCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True