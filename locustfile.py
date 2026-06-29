from locust import HttpUser, task, between
import random

class TodoUser(HttpUser):
    # Simulated wait time between tasks: 0.5 to 1.5 seconds
    wait_time = between(0.5, 1.5)
    
    # Store IDs of tasks created during load test to interact with them
    created_task_ids = []

    def on_start(self):
        """Called when a user starts running."""
        self.created_task_ids = []

    @task(3)
    def list_tasks(self):
        """Simulate listing tasks (high frequency task)."""
        self.client.get("/tasks", name="/tasks (GET)")

    @task(2)
    def create_and_read_task(self):
        """Simulate creating a task, reading it, then editing it."""
        payload = {
            "title": f"Load Test Task {random.randint(1000, 9999)}",
            "description": "Created during performance testing",
            "priority": random.choice(["low", "medium", "high"])
        }
        
        # 1. Create task
        with self.client.post("/tasks", json=payload, name="/tasks (POST)") as response:
            if response.status_code == 201:
                task_id = response.json().get("id")
                if task_id:
                    self.created_task_ids.append(task_id)
                    
                    # 2. Get task detail
                    self.client.get(f"/tasks/{task_id}", name="/tasks/{id} (GET)")
                    
                    # 3. Update task
                    update_payload = {
                        "description": "Updated description during load test",
                        "completed": True
                    }
                    self.client.put(f"/tasks/{task_id}", json=update_payload, name="/tasks/{id} (PUT)")

    @task(1)
    def delete_some_task(self):
        """Simulate deleting a task to maintain DB size."""
        if self.created_task_ids:
            task_id = self.created_task_ids.pop(0)
            self.client.delete(f"/tasks/{task_id}", name="/tasks/{id} (DELETE)")

    @task(1)
    def view_root(self):
        """Simulate hitting the root/welcome page."""
        self.client.get("/", name="/ (GET)")
