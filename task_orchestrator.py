import json
import logging
import os
from agents.task_manager import get_next_task, mark_task_done
from agents.script_generator import generate_script
from agents.code_auditor import review_and_improve
from agents.executor import execute_script
from agents.logger import setup_logging

TASK_FILE = "tasks.json"
CONTEXT_FILE = "context.txt"  # File holding the aggregated context from your codebase



class TaskOrchestrator:
    def __init__(self):
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.tasks = self.load_tasks()
    
    def get_context(self):
        """Reads the latest aggregated context from CONTEXT_FILE."""
        try:
            with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Failed to load context from {CONTEXT_FILE}: {e}")
            return ""
        
    def prepare_prompt(self, task_prompt):
        """Prepends the current context to the task prompt."""
        context = self.get_context()
        full_prompt = f"{context}\n\n{task_prompt}"
        return full_prompt

    def load_tasks(self):
        """Load and parse the tasks.json file."""
        if not os.path.exists(TASK_FILE):
            self.logger.error("tasks.json not found.")
            return []
        try:
            with open(TASK_FILE, "r") as file:
                return json.load(file).get("tasks", [])
        except json.JSONDecodeError:
            self.logger.error("Error reading tasks.json.")
            return []

    def save_tasks(self):
        """Save the updated tasks.json file."""
        try:
            with open(TASK_FILE, "w") as file:
                json.dump({"tasks": self.tasks}, file, indent=4)
        except Exception as e:
            self.logger.error(f"Error saving tasks.json - {e}")

    def process_task(self, task):
        """Process a single task."""
        try:
            task_id = task.get("id")
            prompt = task.get("task")
            file_name = task.get("file_name")
            skip_auditor = task.get("skip_auditor", False)
            execute_flag = task.get("execute", False)
            script_file = f"scripts/script_{task_id}.py"
        except Exception as e:
            self.logger.error(f"Task {task_id}: Error parsing task - {e}")
            return

        full_prompt = self.prepare_prompt(prompt)
        self.logger.info(f"Processing Task {task_id}: {prompt}")

        try:
            # Generate the script
            if not generate_script(full_prompt, script_file, file_name=file_name):
                self.logger.error(f"Task {task_id}: Script generation failed.")
                task["status"] = "failed"
                return

            self.logger.info(f"Task {task_id}: Script generated successfully.")

            # Audit the script if required
            if not skip_auditor:
                script_file = review_and_improve(script_file)
                self.logger.info(f"Task {task_id}: Code reviewed and improved.")

            # Execute the script if flagged
            if execute_flag:
                if execute_script(script_file):
                    self.logger.info(f"Task {task_id}: Execution successful.")
                    task["status"] = "completed"
                else:
                    self.logger.error(f"Task {task_id}: Execution failed.")
                    task["status"] = "execution_failed"
            else:
                self.logger.info(f"Task {task_id}: Execution skipped.")
                task["status"] = "generated_only"

            # Mark task as done
            mark_task_done(task_id)

        except Exception as e:
            self.logger.error(f"Task {task_id}: An error occurred - {e}")
            task["status"] = "error"

    def run(self):
        """Run the task orchestration loop."""
        self.logger.info("Starting task orchestration process...")
        for task in self.tasks:
            if task["status"] == "pending":
                self.process_task(task)
        self.save_tasks()
        self.logger.info("Task processing complete.")
        # Final log line to confirm flush
        self.logger.info("Task processing complete, flushing logs now...")

        # Force a flush
        logging.shutdown()

if __name__ == "__main__":
    orchestrator = TaskOrchestrator()
    orchestrator.run()
