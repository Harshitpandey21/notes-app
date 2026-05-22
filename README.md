# 📝 Notes App — Backend API

A multi-user notes service built with **FastAPI** and **SQLite**. Users can register, log in, create notes, and share them with others.

---

## 🔗 Live URL

```
https://notes-app-hcnp.onrender.com
```

> Interactive API docs: `https://notes-app-hcnp.onrender.com/docs`

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI (Python) |
| Database | SQLite via SQLAlchemy |
| Authentication | JWT (python-jose) |
| Password Hashing | bcrypt (passlib) |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Deployment | Render.com |

---

## ✅ Features

### Core Features
| # | Feature | Method | Endpoint |
|---|---------|--------|----------|
| 1 | Register new user | `POST` | `/register` |
| 2 | User login (JWT) | `POST` | `/login` |
| 3 | Get all notes | `GET` | `/notes` |
| 4 | Get a specific note | `GET` | `/notes/{id}` |
| 5 | Create a note | `POST` | `/notes` |
| 6 | Update a note | `PUT` | `/notes/{id}` |
| 7 | Delete a note | `DELETE` | `/notes/{id}` |
| 8 | Share a note | `POST` | `/notes/{id}/share` |
| 9 | OpenAPI documentation | `GET` | `/openapi.json` |
| 10 | About | `GET` | `/about` |

### Extra Features
| Feature | Method | Endpoint | Description |
|---------|--------|----------|-------------|
| ⭐ Pin / Unpin note | `PATCH` | `/notes/{id}/pin` | Pinned notes always appear at the top of GET /notes |
| 🔍 Full-text search | `GET` | `/search?q=keyword` | Search across title and content of all accessible notes |
| 📄 Pagination | `GET` | `/notes?page=1&page_size=20` | Paginate through notes |

---

## 📖 API Reference

### Register
```http
POST /register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```
**Response:** `201 Created`
```json
{ "message": "User registered successfully" }
```

---

### Login
```http
POST /login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```
**Response:** `200 OK`
```json
{ "access_token": "eyJhbGci..." }
```

---

### Create a Note
```http
POST /notes
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My Note",
  "content": "Note content here"
}
```
**Response:** `201 Created`
```json
{
  "id": "uuid",
  "title": "My Note",
  "content": "Note content here",
  "is_pinned": false,
  "created_at": "2026-01-01T00:00:00",
  "updated_at": "2026-01-01T00:00:00"
}
```

---

### Share a Note
```http
POST /notes/{id}/share
Authorization: Bearer <token>
Content-Type: application/json

{
  "share_with_email": "friend@example.com"
}
```
**Response:** `200 OK`
```json
{ "message": "Note successfully shared with friend@example.com" }
```

---

### Search Notes
```http
GET /search?q=keyword
Authorization: Bearer <token>
```
**Response:** `200 OK` — list of matching notes

---

### Pin / Unpin a Note ⭐
```http
PATCH /notes/{id}/pin
Authorization: Bearer <token>
```
Toggles the pinned state. Pinned notes appear first in `GET /notes`.

---

## 🔒 Authentication

All note endpoints require a JWT token in the header:
```
Authorization: Bearer eyJhbGci...
```

Get your token by calling `POST /login` and copying the `access_token` from the response.

---

## ⭐ Custom Feature — Note Pinning

Users can pin important notes so they always appear at the top of their notes list. Calling `PATCH /notes/{id}/pin` toggles the pin on and off.

**Why this feature?** Real-world note apps like Google Keep and Apple Notes all have pinning because users naturally have a few notes they refer to constantly. It adds immediate practical value with minimal complexity.

---

## 🚀 Running Locally

**Requirements:** Python 3.11+

```bash
# 1. Clone the repository
git clone https://github.com/Harshitpandey21/notes-app.git
cd notes-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file
cp .env

# 4. Start the server
python -m uvicorn main:app --reload
```

App runs at **http://localhost:8000**
Interactive docs at **http://localhost:8000/docs**

---

## 📁 Project Structure

```
notes-app/
├── main.py          # All API endpoints
├── models.py        # Database table definitions
├── schemas.py       # Schema Structure 
├── auth.py          # JWT and password hashing
├── database.py      # Database connection
├── requirements.txt # Python dependencies
├── Dockerfile       # Docker configuration
└── .env             # Environment variable (SECRET_KEY, DATABASE_URL)
```

---

## ⚠️ Edge Cases Handled

- Duplicate email registration returns `409 Conflict`
- Wrong password returns `401 Unauthorized`
- Accessing another user's note returns `403 Forbidden`
- Note not found returns `404 Not Found`
- Sharing a note with yourself returns `400 Bad Request`
- Sharing with a non-existent user returns `404 Not Found`
- Empty title or content is rejected with `422 Unprocessable Entity`
- Password must be at least 6 characters
