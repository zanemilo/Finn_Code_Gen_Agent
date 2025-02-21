import logging
from task_orchestrator import TaskOrchestrator

def main():
    """Main entry point for task processing."""
    orchestrator = TaskOrchestrator()
    orchestrator.run()

if __name__ == "__main__":
    main()
