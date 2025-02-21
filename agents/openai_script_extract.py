import openai
import os
import re
from openai import OpenAI, OpenAIError
from datetime import datetime

class OpenAIScriptExtractor:
    def __init__(self, api_key, model="gpt-4o"):
        """
        Initialize the OpenAI Script Extractor.

        Args:
            api_key (str): Your OpenAI API key.
            model (str): OpenAI model to use (default: gpt-4o).
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def fetch_script(self, prompt, max_tokens=3000, debug_file="debug_response.txt"):
        """
        Fetches a script response from the OpenAI API and saves raw response for debugging.

        Args:
            prompt (str): The user input prompt.
            max_tokens (int): Maximum token limit for the response.
            debug_file (str): Path to save raw API response for debugging.

        Returns:
            str: Extracted script content or None if failed.
        """
        try:
            # Fetch response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
            )

            # Save raw response for debugging
            raw_response = str(response)
            with open(debug_file, "w") as file:
                file.write(raw_response)
            print(f"Raw API response saved to {debug_file}")

            # Access content
            message_content = response.choices[0].message.content
            print("API Response Content:")
            print(message_content)

            # Find all code blocks and filter for Python
            code_blocks = re.findall(r"```(.*?)```", message_content, re.DOTALL)
            for block in code_blocks:
                if block.startswith("python"):
                    script_content = block.replace("python", "", 1).strip()
                    return script_content

            print("No Python script found in the response. Check the raw response.")
            return None

        except Exception as e:
            print(f"Error fetching script: {e}")
            return None

    def strip_response_script(self, response):
        """"""
        # Find all code blocks and filter for Python
        code_blocks = re.findall(r"```(.*?)```", response, re.DOTALL)
        for block in code_blocks:
            if block.startswith("python"):
                script_content = block.replace("python", "", 1).strip()
                return script_content


    def save_script_to_file(self, script_content, output_file):
        """
        Saves the extracted script content to a Python file.

        Args:
            script_content (str): The script text to save.
            output_file (str): Path to save the script file.
        """
        try:
            with open(output_file, 'w') as file:
                file.write(script_content)
            print(f"Script saved to {output_file}")
        except Exception as e:
            print(f"Error saving script to file: {e}")

    def fetch_and_save_script(self, prompt, output_file, max_tokens=3000):
        """
        Fetches a script from the OpenAI API and saves it to a file.

        Args:
            prompt (str): The user input prompt.
            output_file (str): Path to save the script file.
            max_tokens (int): Maximum token limit for the response.
        """
        print("Fetching script from OpenAI...")
        script_content = self.fetch_script(prompt, max_tokens)
        print(script_content)
        if script_content:
            self.save_script_to_file(script_content, output_file)
        else:
            print("Failed to fetch or save script content.")

# Example usage
if __name__ == "__main__":

    date = str(datetime.now())[:10]

    # Replace 'your-api-key-here' with your actual API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key not found in environment variables.")

    extractor = OpenAIScriptExtractor(openai_api_key)

    # Example prompt
    prompt = "Write a Python script framework in a file that can be an abstracted module working off of pyGame to make top down rpg games streamlined by using moudlarization and OOP with best practices."

    # Output file name
    output_file = "generated_" + date + "_script.py"

    # Fetch and save the script
    extractor.fetch_and_save_script(prompt, output_file)
