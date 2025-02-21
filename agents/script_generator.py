import os
import re
from openai_script_extract import OpenAIScriptExtractor

SCRIPT_DIR = "scripts"

def sanitize_filename(task_description):
    """Convert task description into a valid filename."""
    filename = task_description.lower().replace(" ", "_")
    filename = re.sub(r'[^a-z0-9_]', '', filename)  # Remove special characters
    filename = filename.replace("py", "")
    return filename[:50]  # Limit filename length

def generate_unique_filename(base_name):
    """Ensure unique filename by appending numbers if needed."""
    script_path = os.path.join(SCRIPT_DIR, f"{base_name}.py")
    count = 1
    while os.path.exists(script_path):
        script_path = os.path.join(SCRIPT_DIR, f"{base_name}_{count}.py")
        count += 1
    return script_path

def generate_script(prompt, task_description, file_name=None):
    """Generate Python script dynamically based on task description or provided file name."""
    extractor = OpenAIScriptExtractor()

    # If a filename is provided in the task, use it; otherwise, generate one dynamically
    if file_name:
        base_filename = sanitize_filename(file_name)
    else:
        base_filename = sanitize_filename(task_description)

    script_path = generate_unique_filename(base_filename)

    print(f"Generating script: {script_path}")
    
    script_content = extractor.fetch_script(prompt)
    
    with open(script_path, "w", encoding="utf-8") as script_file:
        script_file.write(script_content)
    
    return script_path
