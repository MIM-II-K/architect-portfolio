# API Specification

Base URL:

/api

## Public Endpoints

### Projects

GET /api/projects

GET /api/projects/{slug}

### Categories

GET /api/categories

### Inquiries

POST /api/inquiries

---

## Authentication

POST /api/auth/login

POST /api/auth/logout

POST /api/auth/refresh

---

## Admin Projects

POST /api/projects

PATCH /api/projects/{id}

DELETE /api/projects/{id}

---

## Admin Categories

POST /api/categories

PATCH /api/categories/{id}

DELETE /api/categories/{id}

---

## Admin Inquiries

GET /api/admin/inquiries

PATCH /api/admin/inquiries/{id}

---

## Project Images

POST /api/projects/{id}/images

DELETE /api/projects/{id}/images/{image_id}

---

## Authorization

All admin endpoints require authentication.

Authorization is enforced by the backend.

Frontend route protection alone is not considered security.