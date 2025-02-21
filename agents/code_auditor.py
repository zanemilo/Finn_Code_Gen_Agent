import os
import subprocess
import logging
from openai_python_code_improver import PythonCodeReviewer

# Initialize the code reviewer using the OpenAI API key from the environment
API_KEY = os.getenv("OPENAI_API_KEY")
reviewer = PythonCodeReviewer(api_key=API_KEY)

def run_static_analysis(script_path):
    """
    Run static analysis on the script using flake8 to check for style and common issues.
    
    Returns True if the script passes the checks, False otherwise.
    """
    try:
        # Run flake8 as a subprocess and capture its output
        result = subprocess.run(["flake8", script_path], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"{script_path} passed flake8 checks.")
            return True
        else:
            logging.error(f"Static analysis issues in {script_path}:\n{result.stdout}\n{result.stderr}")
            return False
    except Exception as e:
        logging.exception(f"Error running static analysis on {script_path}: {e}")
        return False

def review_and_improve(script_path):
    """
    Uses the AI-based PythonCodeReviewer to review and improve the script.
    It first optionally runs static analysis before invoking the reviewer.
    
    Returns the path to the improved script if successful, otherwise returns the original script path.
    """
    logging.info(f"Starting review and improvement for {script_path}...")

    # Step 1: Run static analysis; if issues are found, log them (you might decide to halt or continue)
    if not run_static_analysis(script_path):
        logging.warning("Static analysis reported issues. Proceeding with AI-based improvement anyway.")
    
    try:
        # Invoke the PythonCodeReviewer to improve the code.
        reviewer.review_and_improve_code(script_path)
        
        # The reviewer is designed to save an improved version as {original}_improved.py.
        improved_script = script_path.replace(".py", "_improved.py")
        if os.path.exists(improved_script):
            logging.info(f"Improved script available at {improved_script}.")
            return improved_script
        else:
            logging.error("Improved script was not created by the code reviewer.")
            return script_path
    except Exception as e:
        logging.error(f"Error during AI review for {script_path}: {e}")
        return script_path

# If this module is run directly, allow basic testing.
if __name__ == "__main__":
    test_script = "scripts/example_script.py"  # Change to a valid test file path
    improved_path = review_and_improve(test_script)
    print(f"Final script available at: {improved_path}")
