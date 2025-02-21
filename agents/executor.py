import subprocess
import logging

def execute_script(script_path, timeout=10):
    """
    Executes the specified Python script and logs its output.
    Returns True if execution is successful within the timeout, otherwise False.
    """
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True, timeout=timeout)
        logging.info(f"Execution output for {script_path}:\n{result.stdout}")
        if result.returncode == 0:
            logging.info(f"{script_path} executed successfully.")
            return True
        else:
            logging.error(f"{script_path} execution failed:\n{result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logging.warning(f"Execution of {script_path} timed out after {timeout} seconds.")
        return False
    except Exception as e:
        logging.exception(f"Error executing {script_path}: {e}")
        return False

# For standalone testing:
if __name__ == "__main__":
    script = "scripts/script_test.py"
    execute_script(script)
