from sqlalchemy.orm import Session, joinedload
import app.models as models
import app.schemas as schemas
from app.cache import get_user_cache, set_user_cache

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    cached = get_user_cache(email)
    if cached:
        return cached

    user = db.query(models.User).options(joinedload(models.User.tasks))\
        .filter(models.User.email == email).first()

    if user:
        set_user_cache(email, schemas.UserRead.from_orm(user).dict())

    return user

def create_task_for_user(db: Session, user_id: int, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title, user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_users_paginated(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()
