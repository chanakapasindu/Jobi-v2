from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.job import Job
from app.models.user_profile import UserProfile


# Load the embedding model once when the service starts.
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def build_profile_text(profile: UserProfile) -> str:
    return "\n".join(
        [
            f"Skills: {', '.join(profile.skills or [])}",
            f"Education: {', '.join(profile.education or [])}",
            f"Experience: {', '.join(profile.experience or [])}",
            f"Preferred roles: {', '.join(profile.preferred_roles or [])}",
            f"Preferred locations: {', '.join(profile.preferred_locations or [])}",
            f"Employment type: {profile.employment_type or ''}",
            f"Experience level: {profile.experience_level or ''}",
        ]
    )


def build_job_text(job: Job) -> str:
    return "\n".join(
        [
            f"Job title: {job.title}",
            f"Company: {job.company}",
            f"Location: {job.location}",
            f"Description: {job.description or ''}",
        ]
    )


def calculate_semantic_score(profile_text: str, job_text: str) -> float:
    """
    Calculate semantic similarity between a user profile and a job.

    Returns a normalized score between 0.0 and 1.0.
    """
    embeddings = embedding_model.encode(
        [profile_text, job_text],
        normalize_embeddings=True,
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]],
    )[0][0]

    # Cosine similarity can theoretically be negative.
    # Clamp it to our expected 0.0 - 1.0 range.
    return max(0.0, min(1.0, float(similarity)))

def calculate_skill_score(profile: UserProfile, job: Job) -> float:
    """
    Calculate how many of the user's skills are mentioned in the job.

    Returns a normalized score between 0.0 and 1.0.
    """
    profile_skills = [
        skill.strip().lower()
        for skill in (profile.skills or [])
        if skill and skill.strip()
    ]

    if not profile_skills:
        return 0.0

    job_text = build_job_text(job).lower()

    matched_skills = [
        skill
        for skill in profile_skills
        if skill in job_text
    ]

    return len(matched_skills) / len(profile_skills)

def calculate_experience_score(
    profile: UserProfile,
    job: Job,
) -> float:
    """
    Calculate experience-level compatibility.

    The current Job model does not have a dedicated experience-level
    field, so we infer it from the job title and description.
    """
    profile_level = (profile.experience_level or "").strip().lower()

    if not profile_level:
        return 0.0

    job_text = build_job_text(job).lower()

    level_keywords = {
        "intern": ["intern", "internship"],
        "junior": ["junior", "entry level", "entry-level", "graduate"],
        "mid": ["mid", "mid-level", "mid level"],
        "senior": ["senior", "lead", "principal"],
    }

    keywords = level_keywords.get(profile_level, [])

    if not keywords:
        return 0.0

    return 1.0 if any(keyword in job_text for keyword in keywords) else 0.0

def calculate_location_score(
    profile: UserProfile,
    job: Job,
) -> float:
    """
    Calculate location compatibility between the user's preferences
    and the job location.

    Returns 1.0 when the job location matches a preferred location,
    otherwise 0.0.
    """
    preferred_locations = [
        location.strip().lower()
        for location in (profile.preferred_locations or [])
        if location and location.strip()
    ]

    if not preferred_locations:
        return 0.0

    job_location = (job.location or "").strip().lower()

    if not job_location:
        return 0.0

    return 1.0 if any(
        location in job_location or job_location in location
        for location in preferred_locations
    ) else 0.0

def calculate_role_score(
    profile: UserProfile,
    job: Job,
) -> float:
    """
    Calculate whether the job matches one of the user's preferred roles.

    Returns 1.0 for a matching preferred role, otherwise 0.0.
    """
    preferred_roles = [
        role.strip().lower()
        for role in (profile.preferred_roles or [])
        if role and role.strip()
    ]

    if not preferred_roles:
        return 0.0

    job_title = (job.title or "").strip().lower()

    if not job_title:
        return 0.0

    return 1.0 if any(
        role in job_title or job_title in role
        for role in preferred_roles
    ) else 0.0

def calculate_match_score(
    profile: UserProfile,
    job: Job,
) -> float:
    """
    Calculate the final job match score using weighted signals.

    Weights:
    - Semantic similarity: 60%
    - Skill match: 20%
    - Experience level: 10%
    - Location: 5%
    - Preferred role: 5%

    Returns a normalized score between 0.0 and 1.0.
    """
    semantic_score = calculate_semantic_score(
        build_profile_text(profile),
        build_job_text(job),
    )

    skill_score = calculate_skill_score(profile, job)
    experience_score = calculate_experience_score(profile, job)
    location_score = calculate_location_score(profile, job)
    role_score = calculate_role_score(profile, job)

    final_score = (
        semantic_score * 0.60
        + skill_score * 0.20
        + experience_score * 0.10
        + location_score * 0.05
        + role_score * 0.05
    )

    return max(0.0, min(1.0, float(final_score)))

def rank_jobs_for_profile(
    profile: UserProfile,
    jobs: list[Job],
) -> list[tuple[Job, float]]:
    """
    Calculate match scores for all jobs and return them
    sorted from highest score to lowest score.
    """
    scored_jobs = [
        (job, calculate_match_score(profile, job))
        for job in jobs
    ]

    scored_jobs.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return scored_jobs

def generate_recommendation_reasons(
    profile: UserProfile,
    job: Job,
) -> list[str]:
    """
    Generate human-readable reasons explaining why a job
    matches the user's profile.
    """
    reasons = []

    # Preferred role match
    role_score = calculate_role_score(profile, job)
    if role_score > 0:
        reasons.append(
            f"Matches your preferred role: {job.title}"
        )

    # Skill match
    skill_score = calculate_skill_score(profile, job)
    if skill_score > 0:
        reasons.append(
            f"Matches {round(skill_score * 100)}% of your listed skills"
        )

    # Location match
    location_score = calculate_location_score(profile, job)
    if location_score > 0:
        matching_location = next(
            (
                location
                for location in (profile.preferred_locations or [])
                if location.lower() in (job.location or "").lower()
                or (job.location or "").lower() in location.lower()
            ),
            job.location,
        )

        reasons.append(
            f"Matches your preferred location: {matching_location}"
        )

    # Experience match
    experience_score = calculate_experience_score(profile, job)
    if experience_score > 0:
        reasons.append(
            f"Matches your experience level: {profile.experience_level}"
        )

    # Semantic similarity
    semantic_score = calculate_semantic_score(
        build_profile_text(profile),
        build_job_text(job),
    )

    if semantic_score >= 0.5:
        reasons.append("Good semantic match with your profile")
    elif semantic_score >= 0.3:
        reasons.append("Some similarity with your profile")

    # Fallback
    if not reasons:
        reasons.append("Recommended based on overall profile similarity")

    return reasons