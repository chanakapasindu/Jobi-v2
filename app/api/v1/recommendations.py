from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.deps import get_db
from app.models.job import Job
from app.models.user import User
from app.models.user_profile import UserProfile
from app.services.recommendation import (
    rank_jobs_for_profile,
    generate_recommendation_reasons,
)


router = APIRouter()


@router.get("/recommendations")
def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == current_user.id)
        .first()
    )

    if not profile:
        return {
            "recommendations": []
        }

    jobs = db.query(Job).all()

    ranked_jobs = rank_jobs_for_profile(profile, jobs)

    return {
    "recommendations": [
        {
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "match_score": round(score * 100, 2),
            "reasons": generate_recommendation_reasons(profile, job),
        }
        for job, score in ranked_jobs
    ]
}