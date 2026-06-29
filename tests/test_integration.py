import pytest
from fastapi import status
from datetime import datetime, timezone, timedelta

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "Welcome" in response.json()["message"]

def test_create_task_integration(client):
    due_date = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
    task_payload = {
        "title": "Integration Task",
        "description": "API test",
        "priority": "medium",
        "due_date": due_date
    }
    response = client.post("/tasks", json=task_payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Integration Task"
    assert data["id"] is not None
    assert data["completed"] is False
    assert data["is_overdue"] is False

def test_create_task_validation_error(client):
    # Invalid priority
    task_payload = {
        "title": "Invalid Priority Task",
        "priority": "invalid-priority"
    }
    response = client.post("/tasks", json=task_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Past due date
    past_due_date = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
    task_payload_past = {
        "title": "Past Task",
        "due_date": past_due_date
    }
    response = client.post("/tasks", json=task_payload_past)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_tasks_integration(client):
    # Create two tasks
    client.post("/tasks", json={"title": "Task 1", "priority": "low"})
    client.post("/tasks", json={"title": "Task 2", "priority": "high"})
    
    response = client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    
    # Test filters
    response_high = client.get("/tasks?priority=high")
    assert response_high.status_code == status.HTTP_200_OK
    assert len(response_high.json()) == 1
    assert response_high.json()[0]["title"] == "Task 2"

    response_low = client.get("/tasks?priority=low")
    assert response_low.status_code == status.HTTP_200_OK
    assert len(response_low.json()) == 1
    assert response_low.json()[0]["title"] == "Task 1"

    # Test invalid filter
    response_invalid = client.get("/tasks?priority=urgent")
    assert response_invalid.status_code == status.HTTP_400_BAD_REQUEST

def test_get_task_by_id_integration(client):
    # Create task
    post_res = client.post("/tasks", json={"title": "Target Task"})
    task_id = post_res.json()["id"]
    
    # Fetch task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Target Task"

    # Fetch non-existent task
    response_404 = client.get("/tasks/99999")
    assert response_404.status_code == status.HTTP_404_NOT_FOUND

def test_update_task_integration(client):
    # Create task
    post_res = client.post("/tasks", json={"title": "Original Title"})
    task_id = post_res.json()["id"]
    
    # Update task
    update_payload = {"title": "New Title", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "New Title"
    assert data["completed"] is True
    assert data["completed_at"] is not None

    # Update non-existent task
    response_404 = client.put("/tasks/99999", json={"title": "No Task"})
    assert response_404.status_code == status.HTTP_404_NOT_FOUND

def test_delete_task_integration(client):
    # Create task
    post_res = client.post("/tasks", json={"title": "Delete Target"})
    task_id = post_res.json()["id"]
    
    # Delete task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify deletion
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND

    # Delete non-existent task
    response_404 = client.delete("/tasks/99999")
    assert response_404.status_code == status.HTTP_404_NOT_FOUND

def test_complete_task_custom_endpoint_integration(client):
    # Create task
    post_res = client.post("/tasks", json={"title": "To Complete"})
    task_id = post_res.json()["id"]
    
    # Complete task via custom action
    response = client.post(f"/tasks/{task_id}/complete")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["completed"] is True
    assert response.json()["completed_at"] is not None

    # Complete non-existent task
    response_404 = client.post("/tasks/99999/complete")
    assert response_404.status_code == status.HTTP_404_NOT_FOUND
