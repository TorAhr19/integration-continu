import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch
from app import models, crud, schemas

# ==========================================
# 1. PARAMETERIZED TESTS
# ==========================================
# We test check_overdue with multiple due date inputs relative to current time.
@pytest.mark.parametrize(
    "due_offset_seconds, completed, expected_overdue",
    [
        (-10, False, True),   # 10 seconds ago, not completed -> Overdue
        (10, False, False),   # 10 seconds in future, not completed -> Not Overdue
        (-10, True, False),   # 10 seconds ago, completed -> Not Overdue (completed tasks are never overdue)
        (10, True, False),    # 10 seconds in future, completed -> Not Overdue
    ]
)
def test_check_overdue_logic(due_offset_seconds: int, completed: bool, expected_overdue: bool):
    current_time = datetime.now(timezone.utc)
    due_date = current_time + timedelta(seconds=due_offset_seconds)
    
    task = models.Task(
        title="Test Task",
        completed=completed,
        due_date=due_date
    )
    
    assert task.check_overdue(current_time=current_time) == expected_overdue


# Parameterized test for schema priority validation
@pytest.mark.parametrize(
    "priority, should_succeed",
    [
        ("low", True),
        ("LOW", True),
        ("medium", True),
        ("high", True),
        ("HIGH", True),
        ("urgent", False),  # invalid priority
        ("", False),        # empty
    ]
)
def test_priority_validation(priority: str, should_succeed: bool):
    task_data = {
        "title": "Validate Priority",
        "priority": priority,
        "due_date": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    }
    
    if should_succeed:
        schema = schemas.TaskCreate(**task_data)
        assert schema.priority.lower() == priority.lower()
    else:
        with pytest.raises(ValueError):
            schemas.TaskCreate(**task_data)


# ==========================================
# 2. MOCKED TESTS
# ==========================================
# We mock datetime.now inside models.py (or mock standard datetime) to check if is_overdue property uses the mocked time correctly.
def test_is_overdue_property_with_mocked_time():
    # Due date is set to 2026-06-29 12:00:00 UTC
    due_date = datetime(2026, 6, 29, 12, 0, 0, tzinfo=timezone.utc)
    task = models.Task(
        title="Mocked Time Task",
        completed=False,
        due_date=due_date
    )

    # Scenario A: Mock current time to 2026-06-29 11:00:00 (before due date) -> Not overdue
    mock_now_before = datetime(2026, 6, 29, 11, 0, 0, tzinfo=timezone.utc)
    with patch("app.models.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_now_before
        assert task.is_overdue is False

    # Scenario B: Mock current time to 2026-06-29 13:00:00 (after due date) -> Overdue
    mock_now_after = datetime(2026, 6, 29, 13, 0, 0, tzinfo=timezone.utc)
    with patch("app.models.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_now_after
        assert task.is_overdue is True


# ==========================================
# 3. DIRECT UNIT TESTS FOR CRUD LOGIC
# ==========================================
def test_create_task_unit(db_session):
    task_in = schemas.TaskCreate(
        title="Unit Task",
        description="Testing crud create",
        priority="high"
    )
    db_task = crud.create_task(db_session, task_in)
    assert db_task.id is not None
    assert db_task.title == "Unit Task"
    assert db_task.completed is False
    assert db_task.priority == "high"

def test_get_task_unit(db_session):
    # Setup
    task = models.Task(title="Get Unit Task", priority="low")
    db_session.add(task)
    db_session.commit()
    
    # Run
    fetched = crud.get_task(db_session, task.id)
    assert fetched is not None
    assert fetched.id == task.id
    assert fetched.title == "Get Unit Task"

def test_update_task_unit(db_session):
    # Setup
    task = models.Task(title="Original Title", completed=False)
    db_session.add(task)
    db_session.commit()
    
    # Run
    update_data = schemas.TaskUpdate(title="Updated Title", completed=True)
    updated = crud.update_task(db_session, task.id, update_data)
    
    assert updated is not None
    assert updated.title == "Updated Title"
    assert updated.completed is True
    assert updated.completed_at is not None

def test_delete_task_unit(db_session):
    # Setup
    task = models.Task(title="Delete Me")
    db_session.add(task)
    db_session.commit()
    
    # Run
    success = crud.delete_task(db_session, task.id)
    assert success is True
    
    # Confirm
    assert crud.get_task(db_session, task.id) is None

def test_complete_task_unit(db_session):
    # Setup
    task = models.Task(title="Complete Me", completed=False)
    db_session.add(task)
    db_session.commit()
    
    # Run
    completed = crud.complete_task(db_session, task.id)
    assert completed is not None
    assert completed.completed is True
    assert completed.completed_at is not None
