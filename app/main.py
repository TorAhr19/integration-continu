from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, models, schemas
from app.database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo List API",
    description="A simple, robust REST API for managing tasks with priority, due dates, and completion status.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo List API. Visit /docs for documentation."}

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@app.get("/tasks", response_model=List[schemas.TaskResponse])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # If priority is specified, validate it
    if priority is not None:
        priority_lower = priority.lower()
        if priority_lower not in {"low", "medium", "high"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Priority filter must be one of 'low', 'medium', or 'high'"
            )
    return crud.get_tasks(db, skip=skip, limit=limit, completed=completed, priority=priority)

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return None

@app.post("/tasks/{task_id}/complete", response_model=schemas.TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.complete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task
