# 📝 Notes App — Backend API

A multi-user notes service built with **FastAPI** (Python) and **SQLite**.

---

## ✅ Features Implemented

| # | Feature | Endpoint |
|---|---------|----------|
| 1 | Register | `POST /register` |
| 2 | Login (JWT) | `POST /login` |
| 3 | Get all notes | `GET /notes` |
| 4 | Get one note | `GET /notes/{id}` |
| 5 | Create note | `POST /notes` |
| 6 | Update note | `PUT /notes/{id}` |
| 7 | Delete note | `DELETE /notes/{id}` |
| 8 | Share note | `POST /notes/{id}/share` |
| 9 | OpenAPI docs | `GET /openapi.json` |
| 10 | About | `GET /about` |
| ⭐ | **Pin/Unpin note** (custom) | `PATCH /notes/{id}/pin` |
| 🔍 | Full-text search | `GET /search?q=keyword` |
| 📄 | Pagination | `GET /notes?page=1&page_size=20` |

