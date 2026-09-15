# System Architecture

## Overview

The application consists of four primary layers:

1. React frontend
2. FastAPI backend
3. Firebase Firestore database
4. Supabase Storage

## Request Flow

Visitor
    ↓
React Frontend
    ↓
FastAPI REST API
    ↓
Firestore / Supabase Storage

## Frontend

Responsibilities:

- Rendering UI
- Client-side routing
- Form interaction
- API communication
- Admin interface
- Client-side validation

The frontend must not contain server-side secrets.

## Backend

Responsibilities:

- REST API
- Authentication
- Authorization
- Business logic
- Input validation
- Firestore access
- Supabase Storage access
- Error handling
- Logging

## Database

Firebase Firestore stores application data and metadata.

Primary collections:

- projects
- project_images
- categories
- inquiries
- admins

## Storage

Supabase Storage stores project images and profile images.

Firestore stores image metadata and URLs.

## Security Boundary

The browser communicates only with the FastAPI API.

Private credentials remain on the backend.

Admin authorization is enforced by FastAPI.