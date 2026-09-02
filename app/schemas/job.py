from pydantic import BaseModel, Field

class JobCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    company: str = Field(min_length=2, max_length=200)
    location: str = Field(min_length=2, max_length=200)
    description: str | None = None

class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str | None

    class Config:
        from_attributes = True
