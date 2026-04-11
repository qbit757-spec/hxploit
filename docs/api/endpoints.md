# Academic System API Documentation

## Authentication
- `POST /api/v1/auth/register`: Register a new user (default role: profesor).
- `POST /api/v1/auth/login`: Login with username/password to get JWT.

## Students
- `GET /api/v1/students/`: List students (filter by campus).
- `POST /api/v1/students/`: Create a student.
- `GET /api/v1/students/{id}`: Get student details.

## Attendance
- `POST /api/v1/attendance/`: Register/Update attendance for a student.
- `GET /api/v1/attendance/history/{student_code}`: Get student's history from previous cycles.
- `GET /api/v1/attendance/report`: Get attendance reports by campus or cycle.

## Postulations (Public & Review)
- `POST /api/v1/postulations/public/register`: Publicly accessible form to register potential students.
- `GET /api/v1/postulations/`: Admin list of postulations (filtered by status/campus).
- `PATCH /api/v1/postulations/{id}/review`: Approve or Deny a postulation. If approved, student is created.

## Cycles
- `GET /api/v1/cycles/`: List all academic cycles.
- `POST /api/v1/cycles/`: Create a new cycle.
- `POST /api/v1/cycles/{id}/close`: Close the cycle, movings snapshots to history and performing final stats.
