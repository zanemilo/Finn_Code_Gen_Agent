import logging
from task_orchestrator import TaskOrchestrator

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    """Main entry point for task processing."""
    orchestrator = TaskOrchestrator()
    orchestrator.run()

if __name__ == "__main__":
    main()
