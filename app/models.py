from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(String, default="medium")  # low, medium, high
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    def check_overdue(self, current_time: datetime = None) -> bool:
        """
        Business logic to check if a task is overdue.
        Can override current_time for testing/mocking.
        """
        if self.completed or not self.due_date:
            return False
        
        if current_time is None:
            current_time = datetime.now(timezone.utc)
            
        due_date_tz = self.due_date
        if due_date_tz.tzinfo is None:
            due_date_tz = due_date_tz.replace(tzinfo=timezone.utc)
            
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)

        return current_time > due_date_tz

    @property
    def is_overdue(self) -> bool:
        return self.check_overdue()

