from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import json

from database import engine, get_db
import models, schemas
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notes App API",
    description="A multi-user notes service with sharing and search",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Notes App is running. Visit /docs for API documentation."}


@app.get("/about", tags=["About"])
def about():
    return {
        "name": "Harshit Pandey",
        "email": "harshitpandey1234789@gmail.com",
        "my features": {
            "Note Pinning": (
                "Users can pin important notes so they always appear at the top of GET /notes. "
                "Chosen because it mirrors real-world note apps like Google Keep and adds "
                "immediate practical value with minimal complexity."
            ),
            "Full-text Search": (
                "GET /search?q=keyword searches both title and content of notes the user "
                "owns or has access to. Chosen because it becomes essential as a user's "
                "note count grows."
            ),
            "Pagination": (
                "GET /notes supports ?page= and ?page_size= query parameters. "
                "Chosen to keep large responses fast and prevent memory issues at scale."
            ),
        },
    }


@app.post("/register", status_code=status.HTTP_201_CREATED, tags=["Auth"])
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )
    user = models.User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}


@app.post("/login", tags=["Auth"])
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = create_access_token({"sub": user.id})
    return {"access_token": token}


@app.get("/notes", response_model=List[schemas.NoteResponse], tags=["Notes"])
def get_all_notes(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Results per page"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns all notes owned by the user plus notes shared with them.
    Pinned notes appear first, then sorted by updated_at descending.
    Supports pagination via ?page= and ?page_size=.
    """
    owned_ids = {n.id for n in current_user.notes}
    shared_ids = {n.id for n in current_user.shared_notes}
    all_ids = owned_ids | shared_ids

    notes = (
        db.query(models.Note)
        .filter(models.Note.id.in_(all_ids))
        .order_by(models.Note.is_pinned.desc(), models.Note.updated_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return notes


@app.get("/notes/{note_id}", response_model=schemas.NoteResponse, tags=["Notes"])
def get_note(
    note_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    shared_ids = {n.id for n in current_user.shared_notes}
    if note.owner_id != current_user.id and note.id not in shared_ids:
        raise HTTPException(status_code=403, detail="Access denied")

    return note


@app.post("/notes", response_model=schemas.NoteResponse, status_code=status.HTTP_201_CREATED, tags=["Notes"])
def create_note(
    payload: schemas.NoteCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = models.Note(
        title=payload.title,
        content=payload.content,
        owner_id=current_user.id,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@app.put("/notes/{note_id}", response_model=schemas.NoteResponse, tags=["Notes"])
def update_note(
    note_id: str,
    payload: schemas.NoteUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can update this note")

    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content

    db.commit()
    db.refresh(note)
    return note


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Notes"])
def delete_note(
    note_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can delete this note")

    db.delete(note)
    db.commit()


@app.post("/notes/{note_id}/share", tags=["Notes"])
def share_note(
    note_id: str,
    payload: schemas.ShareRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can share this note")

    if payload.share_with_email == current_user.email:
        raise HTTPException(status_code=400, detail="You cannot share a note with yourself")

    target_user = db.query(models.User).filter(models.User.email == payload.share_with_email).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="No user found with that email")

    if target_user in note.shared_with:
        return {"message": f"Note is already shared with {payload.share_with_email}"}

    note.shared_with.append(target_user)
    db.commit()
    return {"message": f"Note successfully shared with {payload.share_with_email}"}


@app.patch("/notes/{note_id}/pin", response_model=schemas.NoteResponse, tags=["Notes"])
def toggle_pin(
    note_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Custom Feature: Pin or unpin a note.
    Pinned notes always appear at the top of GET /notes.
    Only the owner can pin/unpin.
    """
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the owner can pin/unpin this note")

    note.is_pinned = not note.is_pinned
    db.commit()
    db.refresh(note)
    return note


@app.get("/search", response_model=List[schemas.NoteResponse], tags=["Search"])
def search_notes(
    q: str = Query(..., min_length=1, description="Search keyword"),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Full-text search across titles and content of notes the user can access.
    """
    owned_ids = {n.id for n in current_user.notes}
    shared_ids = {n.id for n in current_user.shared_notes}
    all_ids = owned_ids | shared_ids

    keyword = f"%{q}%"
    notes = (
        db.query(models.Note)
        .filter(
            models.Note.id.in_(all_ids),
            or_(
                models.Note.title.ilike(keyword),
                models.Note.content.ilike(keyword),
            ),
        )
        .order_by(models.Note.updated_at.desc())
        .all()
    )
    return notes


@app.get("/openapi.json", include_in_schema=False)
def openapi():
    return app.openapi()
