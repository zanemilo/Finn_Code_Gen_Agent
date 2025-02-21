import logging
import os

def setup_logging(log_file="logs/system.log"):
    """
    Sets up logging to a specified file and the console.
    """
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

# For standalone testing
if __name__ == "__main__":
    setup_logging()
    logging.info("Logger is set up.")
