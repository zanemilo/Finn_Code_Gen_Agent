import os
import json
import re
from agents.logger import setup_logging
import logging

setup_logging(log_file="logs/context_generator.log")
logger = logging.getLogger(__name__)

# Define your shorthand mapping
SHORTHAND_MAP = {
    "class ": "¢",
    "def ": "ƒ",
    "try:": "Ṫ",
    "except ": "Ẋ",
    "logging.error": "ℰ",
    "logging.info": "ℐ",
    "self.": "$",
    "\"\"\"": "∂",
    "return ": "→",
    "import ": "↓",
    "from ": "↘",
    " as ": "≈",
    " with ": "∫",
    " if ": "⊢",
    " else:": "⊣",
    " elif ": "~",
    " for ": "∀",
    " while ": "∃",
    " in ": "∈",
    " not ": "¬",
    " and ": "∧",
    " or ": "∨",
    " is ": "≡",
    " None": "∅",
    " True": "⊤",
    " False": "⊥",
    " pass": "∥",
    " break": "↯",
    " continue": "↺",
    " lambda ": "λ",
    " yield ": "γ",
    " global ": "Ω",
    " nonlocal ": "η"
}

def compress_code1(code):
    # Remove commented lines (lines that start with '#')
    lines = code.splitlines()
    filtered_lines = [line for line in lines if not line.strip().startswith("#")]
    code = "\n".join(filtered_lines)
    
    for pattern, shorthand in SHORTHAND_MAP.items():
        code = code.replace(pattern, shorthand)
    # Refine docstring handling: preserve content between docstring markers
    code = re.sub(r'@DOC(.*?)@DOC', lambda m: f'@DOC {m.group(1).strip()}', code, flags=re.DOTALL)
    return code

def compress_code(code):
    # Split code into lines
    lines = code.splitlines()
    # Filter out comment lines and remove trailing whitespace from each line
    filtered_lines = [line.rstrip() for line in lines if not line.strip().startswith("#")]
    # Remove blank lines
    filtered_lines = [line for line in filtered_lines if line.strip()]
    code = "\n".join(filtered_lines)
    
    # Optional: Condense multiple spaces in non-indented sections
    # Be careful not to disturb leading spaces (indentation) necessary for Python's syntax.
    def condense_spaces(line):
        # Preserve leading spaces and condense the rest
        leading = len(line) - len(line.lstrip())
        return " " * leading + " ".join(line.split())
    
    code = "\n".join(condense_spaces(line) for line in code.splitlines())
    
    # Apply shorthand replacements
    for pattern, shorthand in SHORTHAND_MAP.items():
        code = code.replace(pattern, shorthand)
    
    # Refine docstring handling: preserve content between docstring markers
    code = re.sub(r'@DOC(.*?)@DOC', lambda m: f'@DOC {m.group(1).strip()}', code, flags=re.DOTALL)
    
    return code


def is_valid_py_file(filepath):
    """
    Determine if the file is a valid Python file for context aggregation.
    Excludes files from directories like .git, __pycache__, venv, and env.
    """
    invalid_dirs = {'.git', '__pycache__', 'venv', 'env'}
    parts = set(filepath.split(os.sep))
    return filepath.endswith('.py') and not parts.intersection(invalid_dirs)

def generate_context(root_dir, output_file):
    """
    Recursively reads all .py files from root_dir (excluding unwanted directories)
    and writes their compressed content into output_file with headers indicating the source file.
    """
    aggregated_content = []
    invalid_dirs = {'.git', '__pycache__', 'venv', 'env'}

    # Prepend the shorthand lookup table
    lookup_header = "// SHORTHAND LOOKUP\n" + json.dumps(SHORTHAND_MAP, indent=4) + "\n\n"
    aggregated_content.append(lookup_header)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out unwanted directories
        dirnames[:] = [d for d in dirnames if d not in invalid_dirs]
        for filename in sorted(filenames):
            if filename.endswith('.py'):
                full_path = os.path.join(dirpath, filename)
                if is_valid_py_file(full_path):
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        compressed_content = compress_code(content)
                        header = f"\n# --- {os.path.relpath(full_path, root_dir)} ---\n"
                        aggregated_content.append(header)
                        aggregated_content.append(compressed_content)
                        aggregated_content.append("\n")
                        logger.info(f"Added {full_path} to context.")
                    except Exception as e:
                        logger.error(f"Error reading {full_path}: {e}")

    try:
        with open(output_file, "w", encoding="utf-8") as out_file:
            out_file.write("\n".join(aggregated_content))
        logger.info(f"Context file '{output_file}' created successfully.")
    except Exception as e:
        logger.error(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    # Set the project root directory; adjust if needed.
    project_root = os.path.abspath(".")
    context_file = os.path.join(project_root, "context.txt")
    generate_context(project_root, context_file)
