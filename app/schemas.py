from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone, timedelta
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="The title of the task")
    description: Optional[str] = Field(None, max_length=500, description="Detailed description")
    priority: str = Field("medium", description="Priority level: low, medium, high")
    due_date: Optional[datetime] = Field(None, description="Due date and time for the task")

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        v_lower = v.lower()
        if v_lower not in {"low", "medium", "high"}:
            raise ValueError("Priority must be one of 'low', 'medium', or 'high'")
        return v_lower

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None:
            # Make sure it's aware
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)
            # Check if it is in the past
            now = datetime.now(timezone.utc)
            # Allow minor skew (e.g. 5 seconds) to prevent failing tests due to execution delay
            if v < now - timedelta(seconds=5):
                raise ValueError("Due date must be in the future")
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[str] = Field(None)
    completed: Optional[bool] = Field(None)
    due_date: Optional[datetime] = Field(None)

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v_lower = v.lower()
            if v_lower not in {"low", "medium", "high"}:
                raise ValueError("Priority must be one of 'low', 'medium', or 'high'")
            return v_lower
        return v

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None:
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            if v < now - timedelta(seconds=5):
                raise ValueError("Due date must be in the future")
        return v

class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    completed_at: Optional[datetime] = None
    is_overdue: bool = False

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
