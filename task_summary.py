import json
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Constants
TASKS_FILE = "tasks.json"
WARNING_THRESHOLD = 10

def load_tasks(file_path):
    """Load tasks from a JSON file."""
    if not os.path.exists(file_path):
        logging.error("The tasks file does not exist.")
        return []
    
    try:
        with open(file_path, "r") as file:
            return json.load(file)["tasks"]
    except json.JSONDecodeError:
        logging.error("The tasks file is not a valid JSON.")
        return []

def filter_tasks(tasks, status):
    """Filter tasks by status (e.g., 'pending', 'completed')."""
    return [task for task in tasks if task.get("status") == status]

def summarize_tasks(tasks):
    """Summarize tasks including priority, execution flags, and logging details."""
    total_tasks = len(tasks)
    pending_tasks = filter_tasks(tasks, "pending")
    completed_tasks = filter_tasks(tasks, "completed")

    logging.info(f"Total Tasks: {total_tasks}")
    logging.info(f"Pending Tasks: {len(pending_tasks)}")
    logging.info(f"Completed Tasks: {len(completed_tasks)}")

    if len(pending_tasks) > WARNING_THRESHOLD:
        logging.warning("The number of pending tasks exceeds the threshold!")

    logging.info("\n=== Pending Task Details ===")
    for idx, task in enumerate(pending_tasks, start=1):
        priority = task.get("priority", "None")
        skip_auditor = task.get("skip_auditor", False)
        execute = task.get("execute", False)
        logging.info(f"Task {idx}: {task.get('task', 'Unnamed Task')}")
        logging.info(f"  - Priority: {priority}")
        logging.info(f"  - Skip Auditor: {'Yes' if skip_auditor else 'No'}")
        logging.info(f"  - Execute: {'Yes' if execute else 'No'}")

def main():
    """Main function to execute the task summary module."""
    tasks = load_tasks(TASKS_FILE)
    if tasks:
        summarize_tasks(tasks)
    else:
        logging.info("No tasks available.")

if __name__ == "__main__":
    main()
