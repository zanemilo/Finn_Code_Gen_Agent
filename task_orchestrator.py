import json
import logging
import os
from agents.task_manager import get_next_task, mark_task_done
from agents.script_generator import generate_script
from agents.code_auditor import review_and_improve
from agents.executor import execute_script

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
TASK_FILE = "tasks.json"

class TaskOrchestrator:
    def __init__(self):
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load and parse the tasks.json file."""
        if not os.path.exists(TASK_FILE):
            logging.error("tasks.json not found.")
            return []
        try:
            with open(TASK_FILE, "r") as file:
                return json.load(file).get("tasks", [])
        except json.JSONDecodeError:
            logging.error("Error reading tasks.json.")
            return []

    def save_tasks(self):
        """Save the updated tasks.json file."""
        with open(TASK_FILE, "w") as file:
            json.dump({"tasks": self.tasks}, file, indent=4)

    def process_task(self, task):
        """Process a single task."""
        task_id = task.get("id")
        prompt = task.get("task")
        skip_auditor = task.get("skip_auditor", False)
        execute_flag = task.get("execute", False)
        script_file = f"scripts/script_{task_id}.py"

        logging.info(f"Processing Task {task_id}: {prompt}")

        # Generate the script
        if not generate_script(prompt, script_file):
            logging.error(f"Task {task_id}: Script generation failed.")
            task["status"] = "failed"
            return

        logging.info(f"Task {task_id}: Script generated successfully.")

        # Audit the script if required
        if not skip_auditor:
            script_file = review_and_improve(script_file)
            logging.info(f"Task {task_id}: Code reviewed and improved.")

        # Execute the script if flagged
        if execute_flag:
            if execute_script(script_file):
                logging.info(f"Task {task_id}: Execution successful.")
                task["status"] = "completed"
            else:
                logging.error(f"Task {task_id}: Execution failed.")
                task["status"] = "execution_failed"
        else:
            logging.info(f"Task {task_id}: Execution skipped.")
            task["status"] = "generated_only"

        # Mark task as done
        mark_task_done(task_id)

    def run(self):
        """Run the task orchestration loop."""
        logging.info("Starting task orchestration process...")
        for task in self.tasks:
            if task["status"] == "pending":
                self.process_task(task)
        self.save_tasks()
        logging.info("Task processing complete.")

if __name__ == "__main__":
    orchestrator = TaskOrchestrator()
    orchestrator.run()
