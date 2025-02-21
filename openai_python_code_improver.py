import os
import sys
import openai

# Get the current script directory (agents/)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Move up one level to the project root directory
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(project_root)

# Now import
from openai_script_extract import OpenAIScriptExtractor


class PythonCodeReviewer:
    def __init__(self, api_key, model="gpt-4o"):
        """
        Initialize the Python Code Reviewer.

        Args:
            api_key (str): Your OpenAI API key.
            model (str): OpenAI model to use (default: gpt-4o).
        """
        self.client = openai
        self.client.api_key = api_key
        self.model = model
        self.script_extractor = OpenAIScriptExtractor(api_key, model)

    def review_and_improve_code(self, file_path):
        """
        Reviews and improves the Python code in the specified file.

        Args:
            file_path (str): Path to the Python file to review and improve.
        """
        try:
            # Read the contents of the specified Python file
            with open(file_path, 'r', encoding='utf-8') as file:
                original_code = file.read()

            # Create a prompt for the OpenAI API to review and improve the code
            prompt = f"""Review the following Python code. Provide an improved version using best practices and clean coding principles:

            {original_code}

            Improved Version:
            """

            # Fetch the improved script using the script extractor
            improved_code = self.script_extractor.fetch_script(prompt)

            if not improved_code:
                print("Failed to fetch the improved code from OpenAI.")
                return

            # Define a new file name for the improved version
            improved_file_path = file_path.replace(".py", "_improved.py")

            # Save the improved code to a new file
            self.script_extractor.save_script_to_file(improved_code, improved_file_path)

            print(f"Improved version of '{file_path}' written to '{improved_file_path}'.")

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def main(self, directory=None, file_name=None):
        """
        Main function to prompt user for file review and improvement.
        May take dir and file_name as params
        """
        
        try:
            if not directory:
                # Prompt user for a directory and file name
                directory = input("Enter the directory path: ")
            if not file_name:
                file_name = input("Enter the Python file name: ")

            # Construct full file path
            file_path = os.path.join(directory, file_name)

            # Check if file exists
            if not os.path.isfile(file_path):
                print(f"The file '{file_path}' does not exist.")
                return

            # Run the review and improvement function
            self.review_and_improve_code(file_path)

        except Exception as e:
            print(f"An unexpected error occurred during execution: {e}")

# Example usage
if __name__ == "__main__":
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables.")

    reviewer = PythonCodeReviewer(api_key)

    # Run the main function
    reviewer.main(file_name="")

