# AI Clothes API

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-009688?logo=fastapi&logoColor=white)
![Prisma](https://img.shields.io/badge/Prisma-ORM-2D3748?logo=prisma&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)

A RESTful API for AI-powered garment transformation. Users can upload clothing images and generate new variations using different styles, ambiances, and avatars through AI processing.

## Features

- **JWT Authentication** - Secure user registration and login with bcrypt password hashing
- **Garment Management** - Upload, categorize, and manage clothing images
- **AI Generation** - Transform garments with customizable style, ambiance, and avatar parameters
- **Async Processing** - Background task processing with status tracking (pending/processing/completed/failed)
- **Template System** - Admin-configurable style, ambiance, and avatar prompt templates
- **Docker Support** - One-command deployment with Docker Compose
- **Prisma ORM** - Type-safe database access with PostgreSQL

## Tech Stack

| Category | Technology |
|----------|-----------|
| Framework | FastAPI |
| Language | Python 3.12 |
| Database | PostgreSQL (Supabase) |
| ORM | Prisma Client Python |
| Auth | JWT (python-jose) + bcrypt |
| Storage | Local filesystem (async) |
| Deployment | Docker & Docker Compose |
| Validation | Pydantic |

## Project Structure

```
aiclothes/
├── main.py                  # FastAPI application entry point
├── api/
│   └── routers/
│       ├── auth.py          # Authentication (register, login)
│       ├── users.py         # User CRUD operations
│       ├── garments.py      # Garment upload & management
│       ├── generations.py   # AI generation jobs
│       ├── styles.py        # Style template management
│       ├── ambiances.py     # Ambiance template management
│       └── avatars.py       # Avatar template management
├── core/
│   ├── db.py                # Prisma database connection
│   ├── security.py          # JWT & password utilities
│   ├── ai_service.py        # AI generation service
│   └── storage.py           # File upload handling
├── schemas/                 # Pydantic request/response models
├── prisma/
│   └── schema.prisma        # Database schema definition
├── prompts/                 # AI prompt templates
│   ├── style/
│   ├── ambiance/
│   └── avatar/
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and get JWT token |
| `GET` | `/auth/me` | Get current user info |
| `GET` | `/users` | List all users |
| `GET` | `/users/{id}` | Get user by ID |
| `POST` | `/garments` | Upload a garment image |
| `GET` | `/garments` | List user's garments |
| `GET` | `/garments/{id}` | Get garment details |
| `PUT` | `/garments/{id}` | Update garment metadata |
| `DELETE` | `/garments/{id}` | Delete a garment |
| `POST` | `/generations` | Create AI generation job |
| `GET` | `/generations` | List user's generations |
| `GET` | `/generations/{id}` | Get generation details |
| `GET` | `/generations/{id}/status` | Check generation status |
| `CRUD` | `/styles` | Manage style templates |
| `CRUD` | `/ambiances` | Manage ambiance templates |
| `CRUD` | `/avatars` | Manage avatar templates |

> For detailed request/response examples, see [README_ENDPOINTS.md](README_ENDPOINTS.md)

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL database (or [Supabase](https://supabase.com) account)
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SocialT/aiclothes.git
   cd aiclothes
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secrets
   ```

3. **Option A: Run with Docker (Recommended)**
   ```bash
   docker-compose up --build
   ```

4. **Option B: Run locally**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Set up database
   prisma generate
   prisma db push

   # Start server
   uvicorn main:app --host 0.0.0.0 --port 3000 --reload
   ```

5. **Access the API**
   - API: http://localhost:3000
   - Swagger Docs: http://localhost:3000/docs
   - ReDoc: http://localhost:3000/redoc

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `JWT_SECRET` | Secret key for JWT tokens | `change-me-in-prod` |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `JWT_EXPIRE_MINUTES` | Token expiration time | `60` |
| `BASE_URL` | Server base URL for file URLs | `http://localhost:8000` |
| `UPLOAD_DIR` | Directory for uploaded files | `uploads` |

## Database Schema

The application uses 6 Prisma models:

- **User** - Authentication and profile data
- **Garment** - Uploaded clothing items (belongs to User)
- **Generation** - AI transformation jobs with status tracking (belongs to User, optionally linked to Garment)
- **Style** - Reusable style prompt templates
- **Ambiance** - Reusable ambiance prompt templates
- **Avatar** - Reusable avatar prompt templates

## Roadmap

- [ ] Integrate real AI service (Stable Diffusion / DALL-E / Midjourney)
- [ ] Rate limiting and request throttling
- [ ] Admin dashboard
- [ ] Image optimization and CDN support
- [ ] WebSocket notifications for generation status
- [ ] Role-based access control (RBAC)
- [ ] Unit and integration tests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
