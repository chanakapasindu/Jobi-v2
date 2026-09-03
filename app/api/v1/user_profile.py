from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.deps import get_db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileCreate, UserProfileOut


router = APIRouter()


@router.put("/profile", response_model=UserProfileOut)
def create_or_update_profile(
    payload: UserProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == current_user.id)
        .first()
    )

    if profile:
        profile.skills = payload.skills
        profile.education = payload.education
        profile.experience = payload.experience
        profile.preferred_roles = payload.preferred_roles
        profile.preferred_locations = payload.preferred_locations
        profile.employment_type = payload.employment_type
        profile.experience_level = payload.experience_level
    else:
        profile = UserProfile(
            user_id=current_user.id,
            skills=payload.skills,
            education=payload.education,
            experience=payload.experience,
            preferred_roles=payload.preferred_roles,
            preferred_locations=payload.preferred_locations,
            employment_type=payload.employment_type,
            experience_level=payload.experience_level,
        )
        db.add(profile)

    db.commit()
    db.refresh(profile)

    return profile


@router.get("/profile", response_model=UserProfileOut)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == current_user.id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile