from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from app.database import get_db, engine
import app.models as models
import app.schemas as schemas
import app.crud as crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=list[schemas.UserRead])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users_paginated(db, skip, limit)

@app.get("/users/email/{email}", response_model=schemas.UserRead)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/{user_id}/tasks/", response_model=schemas.TaskRead)
def create_task(user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task_for_user(db, user_id, task)

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000)