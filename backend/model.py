from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from enum import Enum as PyEnum

db = SQLAlchemy()

# Enum for FileType
class FileType(PyEnum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'
    AUDIO = 'AUDIO'
    JSON = 'JSON'
    
# User Model
class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    clerkId = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    is_admin = Column(Boolean, default=False)

    entries = relationship('Entry', backref='user', lazy=True)

# Entry Model
class Entry(db.Model):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True, autoincrement=True)
    entryId = Column(String, unique=True, nullable=False)
    isComplaint = Column(Boolean, nullable=False)
    product = Column(String)
    subProduct = Column(String)
    entryText = Column(Text, nullable=False)
    summary = Column(String)
    fileType = Column(Enum(FileType), nullable=False, default=FileType.TEXT)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    userId = Column(Integer, ForeignKey('user.id'), nullable=False)