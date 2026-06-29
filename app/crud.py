from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Optional
from app import models, schemas

def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100, completed: Optional[bool] = None, priority: Optional[str] = None) -> List[models.Task]:
    query = db.query(models.Task)
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    if priority is not None:
        query = query.filter(models.Task.priority == priority.lower())
    return query.offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority.lower(),
        due_date=task.due_date
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate) -> Optional[models.Task]:
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        if key == "completed":
            db_task.completed = value
            if value:
                db_task.completed_at = datetime.now(timezone.utc)
            else:
                db_task.completed_at = None
        else:
            setattr(db_task, key, value)
            
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int) -> bool:
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True

def complete_task(db: Session, task_id: int) -> Optional[models.Task]:
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    db_task.completed = True
    db_task.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_task)
    return db_task
