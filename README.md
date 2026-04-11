# Academic System Backend - HXPLOIT

Professional FastAPI backend for academic management, student attendance tracking, and public enrollments with automated validation rules.

## Features

- **Advanced Role-Based Auth**: Username-based authentication (No email required).
- **Attendance Management**: Multi-campus attendance tracking with academic cycles.
- **Automated Validation**: Filter students with 3+ absences from previous cycles during new enrollment.
- **Cycle Control**: Close academic periods to archive history and generate snapshots.
- **Containerized**: Fully Dockerized for production availability.
- **Auto-generated Documentation**: Swagger/OpenAPI documentation at `/docs`.

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy Async
- **Security**: JWT & Passlib (bcrypt)
- **Deployment**: Docker & Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose installed.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/qbit757-spec/hxploit.git
   cd hxploit
   ```

2. Setup environment variables:
   ```bash
   cp .env.example .env
   ```

3. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

The API will be available at `http://localhost:8000`.

## Documentation

Comprehensive API documentation is available at `/docs` once the server is running. You can also find a summary in [docs/api/endpoints.md](docs/api/endpoints.md).

## Default Admin Credentials

- **Username**: `admin`
- **Password**: `admin123`
