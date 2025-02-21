# Autonomous Code Generation Agent System - FINN

## Overview

This project is an autonomous agent system that generates, reviews, audits, and executes Python scripts using OpenAI's GPT models. It processes tasks in a structured pipeline that includes:

- **Script Generation:** Uses OpenAI API to generate Python code from a natural language prompt.
- **Code Auditing and Improvement:** Combines static analysis (flake8) and AI-based code review to improve code quality.
- **Script Execution:** Runs the generated scripts in a controlled environment.
- **Logging and Reporting:** Logs all actions and generates a summary report for each task.
- **Task Management:** Reads and updates tasks from a JSON file (`tasks.json`).

## Features

- **Dynamic Task Execution:** Reads and executes tasks dynamically from `tasks.json`.
- **Automated Code Review:** Uses AI and static analysis to ensure high code quality.
- **Controlled Execution Environment:** Runs scripts safely and logs results.
- **Integration with OpenAI API:** Uses AI to enhance script generation and review.
- **Logging System:** Detailed logs and summary reports for transparency.

## Requirements

- Python 3.8+
- OpenAI API Key (set as the environment variable `OPENAI_API_KEY`)
- Required packages:
  - `openai`
  - `flake8`

Install required dependencies using:

```bash
pip install openai flake8
```

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Set the OpenAI API Key:**
   - Linux/macOS:
     ```bash
     export OPENAI_API_KEY="your-api-key"
     ```
   - Windows:
     ```cmd
     set OPENAI_API_KEY="your-api-key"
     ```

3. **Project Structure:**

   ```
   project/
   ├── agents/
   │   ├── code_auditor.py         # Audits and improves generated scripts
   │   ├── executor.py             # Executes generated scripts
   │   ├── logger.py               # Handles logging
   │   ├── script_generator.py     # Generates Python scripts using OpenAI
   │   └── task_manager.py         # Manages tasks stored in tasks.json
   ├── logs/
   │   ├── system.log              # System logs
   │   └── report.log              # Summary report log
   ├── scripts/                    # Folder for generated scripts
   ├── tasks.json                  # JSON file containing tasks
   ├── openai_python_code_improver.py  # AI-based code review module
   ├── openai_script_extract.py    # Extracts OpenAI responses
   ├── main.py                     # Main orchestration file
   ```

## Usage

1. **Add Tasks:**  
   Update `tasks.json` with new tasks. Example:
   ```json
   {
       "tasks": [
           {
               "id": 1,
               "task": "Create a Python script that prints 'Hello, World!'",
               "priority": "high",
               "status": "pending"
           }
       ]
   }
   ```

2. **Run the System:**
   ```bash
   python main.py
   ```

3. **Monitor Logs:**
   - Detailed logs in `logs/system.log`
   - Summary reports in `logs/report.log`

When all tasks are completed, the system logs the completion and exits.

## Known Issues & Limitations

### 1. **File Not Found Errors During Static Analysis**
   - **Issue:** Some scripts fail during static analysis due to missing files or incorrect paths.
   - **Cause:** The system attempts to run `flake8` on a script that may not exist or is improperly referenced.
   - **Solution:** Add a file existence check before executing static analysis.

### 2. **Tasks.json Not Properly Parsed**
   - **Issue:** Errors such as `AttributeError: 'str' object has no attribute 'get'` occur.
   - **Cause:** The task file may be read incorrectly as a string instead of a dictionary.
   - **Solution:** Ensure proper JSON parsing and validation before processing tasks.

### 3. **Execution Failure Due to Script Logic Issues**
   - **Issue:** Some generated scripts fail during execution due to undefined variables or incorrect imports.
   - **Solution:** Improve AI prompts for script generation to ensure better structure and handling of dependencies.

### 4. **Repetitive Task Regeneration**
   - **Issue:** Tasks that fail execution are sometimes regenerated repeatedly without fixing the root cause.
   - **Solution:** Introduce an error-handling mechanism to modify or improve failing tasks before retrying.

### 5. **Logging Needs Refinement**
   - **Issue:** Some error messages are too vague to diagnose issues properly.
   - **Solution:** Improve logging by including more context and debugging information in failure cases.

## Future Improvements

- **Enhanced Error Handling:** Better management of failed executions.
- **Improved AI Prompts:** Fine-tuned prompt engineering for better script generation.
- **Docker Integration:** Run scripts in isolated environments.
- **GUI Dashboard:** Provide a web-based interface for task monitoring.

## Contributing

Contributions, feature requests, and bug reports are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [OpenAI](https://openai.com) for GPT models.
- Various open-source tools such as flake8 for static analysis.
