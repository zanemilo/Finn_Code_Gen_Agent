# Autonomous Code Generation Agent System - FINN

## Overview

FINN is an autonomous agent system designed to generate, audit, execute, and improve Python scripts using OpenAI's GPT models. It processes tasks dynamically, ensuring structured execution and intelligent refinement.

### **Core Functionalities**

- **Dynamic Task Management:** Reads and executes tasks dynamically from `tasks.json`, updating statuses accordingly.
- **AI-Powered Code Generation & Review:** Uses OpenAI's API to generate scripts and improve code quality based on best practices.
- **Secure & Controlled Execution:** Ensures safe script execution with logging and error tracking.
- **Comprehensive Logging & Reporting:** Logs all actions and provides detailed task summaries for transparency.

## Features

### ✅ **Enhanced AI-Based Code Improvement**  
- Uses `openai_python_code_improver.py` and `openai_script_extract.py` for structured script enhancement.
- Debugging mechanisms allow for improved accuracy in AI-generated code.

### ✅ **Dynamic Task Management**  
- Loads tasks from `tasks.json`, processes them, and updates statuses efficiently.

### ✅ **Robust Logging & Reporting**  
- Logs execution flow in `logs/system.log` and task summaries in `logs/report.log`.
- Improved log flushing ensures all information is captured properly.

### ✅ **Improved OpenAI Integration**  
- Extracts and refines AI-generated code with better response parsing.
- Saves raw API responses for debugging to enhance script extraction.

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
   git clone https://github.com/zanemilo/Finn_Code_Gen_Agent
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
   ├── task_orchestrator.py        # Handles execution flow
   ├── task_summary.py             # Summarizes task progress
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
               "status": "pending",
               "execute": false,
               "file_name": "script_name.py"
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

## Known Issues & Limitations

### **Resolved Issues**
✅ *Tasks.json Parsing Errors Fixed*  
✅ *Logging System Improved for Better Debugging*  
✅ *Refined AI-Based Code Review for Enhanced Code Quality*  

### **Current Limitations**
❌ *Automated Task Scheduling Needed*  
❌ *GUI Dashboard for Task Monitoring Could Improve Usability*  
❌ *Advanced Error Recovery Mechanisms Still in Development*  
❌ *Automated Code Execution is Non-functional*  
  

## Future Improvements

- **Automated Task Scheduling** – Implementing periodic execution for scheduled tasks.
- **Automated Task Auditing/Updating** – Review previously output tasks scripts, alter tasks.json task prompts to fine tune future outputs.
- **Contextual Processing** – Create middleman agent to oversee script/task production by verifying context of overall goal by verifying summary, logs, and scripts to align with goal.
- **GUI Dashboard** – A web-based interface for real-time task monitoring.
- **Enhanced Error Handling** – More robust recovery mechanisms for failed executions.
- **Automated Task Auditing/Updating** – Refine and refactor code base, ensuring maintainability.
- **Rolling Context Window** – Implement a rolling context window that only retains the most recent and relevant interactions. This will reduce token usage and improve performance by dynamically pruning outdated context.
- **Log Clean-Up** – Enhance the logging system to automatically clean up redundant or unnecessary log entries. This will help maintain clarity and manageability of log files over time.
- **Refined Context Generation** – Update the context generator to ignore itself and filter out irrelevant files (e.g., test files, temporary files, and non-essential modules). This will ensure that only pertinent code is aggregated into the context file, improving accuracy and efficiency.
- **Improved File Filtering** – Fine-tune file scanning logic to detect and skip files that should not be included, preventing the context generator from processing its own scripts and other extraneous content.

## Contributing

Contributions, feature requests, and bug reports are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [OpenAI](https://openai.com) for GPT models.
- Various open-source tools such as flake8 for static analysis.
