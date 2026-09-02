# 🚀 Jobi – AI-Ready Job Management Backend

A production-structured **FastAPI** backend for **job posting** and **user authentication**, built with **Docker**, **PostgreSQL**, **JWT auth**, and **Alembic migrations**.

Designed as a scalable foundation for future **AI-powered job recommendation** features.

---

## 🏗 Tech Stack

- Python 3.13  
- FastAPI  
- PostgreSQL 16  
- SQLAlchemy 2.0  
- Alembic  
- JWT (python-jose)  
- Passlib (bcrypt)  
- Docker & Docker Compose  
- Git (feature-branch workflow)

---

## 📂 Project Structure

```txt
Jobi/
│
├── alembic/                     # Database migration system
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── api/v1/                  # Versioned API routes
│   │   ├── auth.py
│   │   ├── jobs.py
│   │   └── router.py
│   │
│   ├── core/                    # Configuration & security logic
│   │   ├── auth.py              # get_current_user dependency
│   │   ├── config.py            # Settings loader
│   │   └── security.py          # JWT & password hashing
│   │
│   ├── db/                      # Database configuration
│   │   ├── session.py
│   │   ├── deps.py
│   │   ├── init_db.py
│   │   └── test_db.py
│   │
│   ├── models/                  # SQLAlchemy models
│   │   ├── user.py
│   │   └── job.py
│   │
│   ├── schemas/                 # Pydantic request/response models
│   │   ├── user.py
│   │   ├── job.py
│   │   └── token.py
│   │
│   ├── services/                # Business logic layer
│   │
│   └── main.py                  # FastAPI entry point
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

- User registration  
- Secure password hashing using **bcrypt**  
- JWT access token generation  
- OAuth2 password flow  
- Protected routes  
- Current authenticated user endpoint  

#### Authentication Endpoints

| Method | Endpoint                | Description                    |
|--------|------------------------|--------------------------------|
| POST   | `/api/v1/auth/register` | Register a new user            |
| POST   | `/api/v1/auth/login`    | Login & receive JWT token      |
| GET    | `/api/v1/auth/me`       | Get current authenticated user |

---

### 💼 Job Management

- Create job (**authenticated users only**)  
- List jobs  
- Search jobs via query parameters  
- Filter by:
  - Location
  - Company  
- Pagination using `limit` and `offset`

#### Job Endpoints

| Method | Endpoint        | Description               |
|--------|-----------------|---------------------------|
| POST   | `/api/v1/jobs/` | Create job (protected)    |
| GET    | `/api/v1/jobs/` | List & search jobs        |

#### Search Example

```http
GET /api/v1/jobs/?q=engineer&location=London&limit=10&offset=0
```

---

### 🩺 Health Check

| Method | Endpoint         | Description        |
|--------|------------------|-------------------|
| GET    | `/api/v1/health` | API health check  |

---

## 🗄 Database Design

- PostgreSQL 16  
- SQLAlchemy Declarative ORM  
- Alembic migration tracking  
- Version-controlled schema via `alembic_version` table  

### Core Entities

- **User**
- **Job**

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

| File               | Purpose               |
|--------------------|-----------------------|
| `.env`             | Local development     |
| `.env.docker`      | Docker development    |
| `.env.*.example`   | Safe template in Git  |

✅ Real `.env` files are ignored and never committed.

### Important Environment Variables

- `DATABASE_URL`
- `JWT_SECRET`

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

### 3️⃣ Run Application

```bash
uvicorn app.main:app --reload
```

Access API documentation:

```
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

```
http://localhost:8000/docs
```

---

## ⚡ Quick Start (Docker)

```bash
docker compose up --build
docker compose exec api alembic upgrade head
```

Then open:

```
http://localhost:8000/docs
```

---

## 🔀 Development Workflow

This project follows a structured feature-branch strategy:

- `feature/authentication`
- `feature/jobs`
- `feature/jobs-search`
- `feature/migrations`
- `feature/docker`

Only stable features are merged into `main`.

---

## 🔐 Security Practices

- Secrets are never committed  
- `.env` files are ignored  
- Passwords hashed using **bcrypt**  
- JWT-based stateless authentication  
- Dependency-based route protection  
- Production-style migration control  
- `.dockerignore` prevents unnecessary files from being copied into the Docker image  

---

## 🧠 Future Roadmap

- Role-based access control  
- Refresh tokens  
- Resume upload & parsing  
- AI-powered job recommendation engine  
- Resume-job semantic matching  
- CI/CD pipeline  
- Cloud deployment (AWS / GCP)  
- Reverse proxy (Nginx)  
- Monitoring & logging integration  

---

## 🎯 Why This Project

This project demonstrates:

- Clean backend architecture  
- Secure authentication design  
- Database modeling & migrations  
- Dockerized environment setup  
- Structured Git workflow  
- Scalable API design patterns  

It forms a strong foundation for production-grade backend systems and future AI integration.

---

## 👤 Author

**R.A. Pasindu Chanaka Ranasingha**  
Software Engineering Undergraduate  
Future MSc AI Candidate  

---

## 📄 License

Developed for educational and portfolio purposes.
