import json
import os

# File where tasks are stored
TASK_FILE = "tasks.json"

def load_tasks():
    """
    Load tasks from the JSON file.
    
    Returns:
        dict: A dictionary containing the tasks.
    """
    if not os.path.exists(TASK_FILE):
        return {"tasks": []}
    with open(TASK_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    """
    Save tasks to the JSON file.
    
    Args:
        tasks (dict): A dictionary containing the tasks to be saved.
    """
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(task):
    """
    Add a new task to the task list.
    
    Args:
        task (dict): A dictionary representing the task to be added.
    """
    tasks = load_tasks()
    tasks.setdefault("tasks", []).append(task)
    save_tasks(tasks)

def get_next_task():
    """
    Get the next pending task.
    
    Returns:
        dict or None: The next pending task if available, otherwise None.
    """
    tasks = load_tasks()
    for task in tasks.get("tasks", []):
        if task.get("status") == "pending":
            return task
    return None

def mark_task_done(task_id):
    """
    Mark a task as completed.
    
    Args:
        task_id (int): The ID of the task to be marked as completed.
    """
    tasks = load_tasks()
    for task in tasks.get("tasks", []):
        if task.get("id") == task_id:
            task["status"] = "completed"
    save_tasks(tasks)
