# 🚀 Jobi – AI-Powered Job Management Backend

A production-structured **FastAPI** backend for **job posting, user authentication, user profiles, and AI-powered job recommendations**, built with **PostgreSQL**, **SQLAlchemy**, **Alembic**, **JWT authentication**, and **Sentence Transformers**.

Jobi is designed as a scalable backend foundation for intelligent job matching and recommendation features.

---

## 🏗 Tech Stack

* Python 3.13
* FastAPI
* PostgreSQL 16
* SQLAlchemy 2.0
* Alembic
* JWT (`python-jose`)
* Passlib (`bcrypt`)
* Sentence Transformers
* Scikit-learn
* Docker & Docker Compose
* Git (feature-branch workflow)

---

## 📂 Project Structure

```text
Jobi/

│
├── alembic/                         # Database migration system
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── api/v1/                      # Versioned API routes
│   │   ├── auth.py
│   │   ├── jobs.py
│   │   ├── user_profile.py
│   │   ├── recommendations.py
│   │   └── router.py
│   │
│   ├── core/                        # Configuration & security logic
│   │   ├── auth.py                  # Current user authentication
│   │   ├── config.py                # Settings loader
│   │   └── security.py              # JWT & password hashing
│   │
│   ├── db/                          # Database configuration
│   │   ├── session.py
│   │   ├── deps.py
│   │   ├── init_db.py
│   │   └── test_db.py
│   │
│   ├── models/                      # SQLAlchemy models
│   │   ├── user.py
│   │   ├── job.py
│   │   └── user_profile.py
│   │
│   ├── schemas/                     # Pydantic request/response models
│   │   ├── user.py
│   │   ├── job.py
│   │   ├── token.py
│   │   └── user_profile.py
│   │
│   ├── services/                    # Business logic
│   │   └── recommendation.py        # AI recommendation engine
│   │
│   └── main.py                      # FastAPI entry point
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── .env
├── .env.docker
├── .env.local.example
├── .env.docker.example
├── .gitignore
└── README.md
```

---

## ✨ Features

### 🔐 Authentication

* User registration
* Secure password hashing using **bcrypt**
* JWT access token generation
* OAuth2 password flow
* Protected routes
* Current authenticated user endpoint

#### Authentication Endpoints

| Method | Endpoint                | Description                    |
| ------ | ----------------------- | ------------------------------ |
| POST   | `/api/v1/auth/register` | Register a new user            |
| POST   | `/api/v1/auth/login`    | Login and receive JWT token    |
| GET    | `/api/v1/auth/me`       | Get current authenticated user |

---

### 💼 Job Management

* Create jobs (**authenticated users only**)
* List jobs
* Search jobs using query parameters
* Filter by:

  * Location
  * Company
* Pagination using `limit` and `offset`

#### Job Endpoints

| Method | Endpoint        | Description          |
| ------ | --------------- | -------------------- |
| POST   | `/api/v1/jobs/` | Create job           |
| GET    | `/api/v1/jobs/` | List and search jobs |

#### Search Example

```http
GET /api/v1/jobs/?q=engineer&location=London&limit=10&offset=0
```

---

### 👤 User Profile

Users can maintain a structured profile that is used by the recommendation engine.

Profile information includes:

* Skills
* Education
* Experience
* Preferred roles
* Preferred locations
* Employment type
* Experience level

#### User Profile Endpoints

| Method | Endpoint          | Description                   |
| ------ | ----------------- | ----------------------------- |
| PUT    | `/api/v1/profile` | Create or update user profile |
| GET    | `/api/v1/profile` | Get current user's profile    |

---

### 🤖 AI Job Recommendation Engine

Jobi currently includes a **hybrid AI recommendation system** that combines semantic similarity with rule-based matching signals.

The recommendation engine uses **Sentence Transformers** to generate text embeddings and calculate semantic similarity between the user's profile and available jobs.

#### Recommendation Signals

| Signal                    | Weight |
| ------------------------- | -----: |
| Semantic similarity       |    60% |
| Skill matching            |    20% |
| Experience-level matching |    10% |
| Location matching         |     5% |
| Preferred-role matching   |     5% |

The final score is calculated internally between `0.0` and `1.0` and returned by the API as a percentage between `0` and `100`.

#### Recommendation Pipeline

```text
User Profile
      ↓
Profile Text Construction
      ↓
Sentence Transformer Embeddings
      ↓
Semantic Similarity
      +
Skill Matching
      +
Experience Matching
      +
Location Matching
      +
Role Matching
      ↓
Weighted Match Score
      ↓
Job Ranking
      ↓
Recommendation Reasons
      ↓
FastAPI Recommendation Endpoint
```

#### Recommendation Endpoint

| Method | Endpoint                  | Description                          |
| ------ | ------------------------- | ------------------------------------ |
| GET    | `/api/v1/recommendations` | Get personalized job recommendations |

The endpoint is protected and uses the currently authenticated user's profile.

#### Example Response

```json
{
  "recommendations": [
    {
      "job_id": 3,
      "title": "java Developer",
      "company": "ABC",
      "location": "Colombo",
      "match_score": 37.92,
      "reasons": [
        "Matches your preferred location: Colombo",
        "Good semantic match with your profile"
      ]
    }
  ]
}
```

The recommendation response includes both a **match percentage** and human-readable **recommendation reasons**.

---

### 🩺 Health Check

| Method | Endpoint         | Description      |
| ------ | ---------------- | ---------------- |
| GET    | `/api/v1/health` | API health check |

---

## 🗄 Database Design

* PostgreSQL 16
* SQLAlchemy Declarative ORM
* Alembic migration tracking
* Version-controlled schema using the `alembic_version` table

### Core Entities

* **User**
* **Job**
* **UserProfile**

### User Profile Relationship

```text
User
 │
 └── UserProfile
       ├── Skills
       ├── Education
       ├── Experience
       ├── Preferred Roles
       ├── Preferred Locations
       ├── Employment Type
       └── Experience Level
```

Each user has at most one profile.

All schema changes are managed using **Alembic migrations**.

---

## 🔄 Database Migrations

### Create a Migration

```bash
alembic revision --autogenerate -m "describe change"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Downgrade Migration

```bash
alembic downgrade -1
```

---

## ⚙️ Environment Configuration

This project separates environment settings for security and flexibility.

| File             | Purpose                            |
| ---------------- | ---------------------------------- |
| `.env`           | Local development                  |
| `.env.docker`    | Docker development                 |
| `.env.*.example` | Safe environment templates for Git |

✅ Real `.env` files are ignored and never committed.

### Important Environment Variables

* `DATABASE_URL`
* `JWT_SECRET`

---

## 🖥 Local Development Setup

### 1️⃣ Create Environment File

**Windows**

```bash
copy .env.local.example .env
```

**Mac/Linux**

```bash
cp .env.local.example .env
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Apply Database Migrations

```bash
alembic upgrade head
```

### 4️⃣ Run Application

```bash
uvicorn app.main:app --reload
```

Access the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🐳 Docker Setup

### 1️⃣ Create Docker Environment File

```bash
copy .env.docker.example .env.docker
```

### 2️⃣ Build and Run Containers

```bash
docker compose up --build
```

### 3️⃣ Run Migrations Inside Container

```bash
docker compose exec api alembic upgrade head
```

### 4️⃣ Access API

```text
http://localhost:8000/docs
```

---

## ⚡ Quick Start

```bash
docker compose up --build

docker compose exec api alembic upgrade head
```

Then open:

```text
http://localhost:8000/docs
```

---

## 🔀 Development Workflow

This project follows a structured **feature-branch Git workflow**.

Example feature branches:

```text
feature/authentication
feature/jobs
feature/jobs-search
feature/migrations
feature/docker
feature/ai-job-recommendation
```

Features are developed and tested in dedicated branches before being merged into the main stable branch.

---

## 🔐 Security Practices

* Secrets are never committed
* `.env` files are ignored
* Passwords are hashed using **bcrypt**
* JWT-based stateless authentication
* Protected routes use authentication dependencies
* Database schema changes are controlled through Alembic migrations
* `.dockerignore` prevents unnecessary files from being copied into Docker images

---

## 🧠 Current AI Recommendation Capabilities

The current recommendation engine supports:

* User profile-based recommendations
* Sentence Transformer embeddings
* Semantic profile-to-job similarity
* Skill matching
* Experience-level matching
* Preferred-location matching
* Preferred-role matching
* Weighted hybrid scoring
* Ranked job recommendations
* Human-readable recommendation reasons
* Authenticated recommendation requests

---

## 🛣️ Future Roadmap

* Improve semantic and skill matching accuracy
* Add richer job metadata
* Resume upload and parsing
* Resume-to-job semantic matching
* Recommendation feedback / "Not Interested"
* Recommendation history
* Pagination and filtering for recommendations
* Background embedding generation
* Embedding caching
* Vector database / vector storage
* Role-based access control
* Refresh tokens
* CI/CD pipeline
* Cloud deployment (AWS / GCP)
* Reverse proxy (Nginx)
* Monitoring and logging integration

---

## 🎯 Why This Project

Jobi demonstrates practical backend engineering and AI integration concepts, including:

* Clean FastAPI architecture
* Secure authentication
* PostgreSQL database design
* SQLAlchemy ORM
* Alembic database migrations
* Dockerized development
* REST API design
* Feature-branch Git workflow
* User profile modeling
* Semantic embeddings
* Hybrid recommendation algorithms
* Explainable recommendation results

The project provides a foundation for building a production-oriented **AI-powered job matching platform**.

---

## 👤 Author

**R.A. Pasindu Chanaka Ranasingha**

Software Engineering Undergraduate

Future MSc AI Candidate

---

## 📄 License

Developed for educational and portfolio purposes.
