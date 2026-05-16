from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from database import Base


def generate_uuid():
    return str(uuid.uuid4())

shared_notes = Table(
    "shared_notes",
    Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("note_id", String, ForeignKey("notes.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    notes = relationship("Note", back_populates="owner", cascade="all, delete-orphan")
    shared_notes = relationship("Note", secondary=shared_notes, back_populates="shared_with")


class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    is_pinned = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="notes")
    shared_with = relationship("User", secondary=shared_notes, back_populates="shared_notes")
