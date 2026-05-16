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

---

## 🚀 Deploy to Render.com (Free — Recommended)

> Render gives you a free server that stays alive. Takes ~5 minutes.

### Step 1 — Put your code on GitHub

1. Go to [github.com](https://github.com) → Sign up / Log in
2. Click the **+** button → **New repository**
3. Name it `notes-app`, click **Create repository**
4. On your computer, open a terminal and run:

```bash
cd notes-app
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/notes-app.git
git push -u origin main
```
> Replace `YOUR_USERNAME` with your GitHub username.

---

### Step 2 — Deploy on Render

1. Go to [render.com](https://render.com) → Sign up with GitHub
2. Click **New +** → **Web Service**
3. Connect your `notes-app` repository
4. Fill in these settings:
   - **Name:** `notes-app` (or anything you like)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Advanced** → **Add Environment Variable**:
   - Key: `SECRET_KEY`
   - Value: any long random string, e.g. `my-super-secret-key-12345-abcdef`
6. Click **Create Web Service**

Wait ~2 minutes. Your app will be live at:
```
https://notes-app-xxxx.onrender.com
```

---

### Step 3 — Update /about with your name

Open `main.py`, find the `/about` endpoint and replace:
```python
"name": "Your Name",
"email": "your.email@example.com",
```
with your actual name and email, then `git push` again.

---

## 🏃 Run Locally

```bash
# 1. Install Python 3.11+ from python.org

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy env file
cp .env.example .env

# 4. Start the server
uvicorn main:app --reload

# App runs at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

---

## 📖 API Quick Reference

### Register
```
POST /register
{"email": "you@example.com", "password": "yourpass"}
```

### Login → get token
```
POST /login
{"email": "you@example.com", "password": "yourpass"}
→ {"access_token": "eyJ..."}
```

### Use token in all note requests
```
Header: Authorization: Bearer eyJ...
```

### Create a note
```
POST /notes
{"title": "Shopping list", "content": "Milk, eggs, bread"}
```

### Share a note
```
POST /notes/{id}/share
{"share_with_email": "friend@example.com"}
```

### Pin a note (custom feature ⭐)
```
PATCH /notes/{id}/pin
→ Toggles pinned state. Pinned notes appear first in GET /notes.
```

### Search notes
```
GET /search?q=shopping
```

### Paginate notes
```
GET /notes?page=2&page_size=10
```

---

## 🐳 Docker (Optional)

```bash
docker build -t notes-app .
docker run -p 8000:8000 -e SECRET_KEY=mysecret notes-app
```

---

## 🏗 Tech Stack

- **FastAPI** — web framework
- **SQLite** — database (file-based, no setup needed)
- **SQLAlchemy** — database ORM
- **python-jose** — JWT tokens
- **passlib + bcrypt** — password hashing
- **Pydantic** — data validation
