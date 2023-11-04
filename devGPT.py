import os
import json
import openai
import random
import re

class UnifiedChatGPTApiClient:
    def __init__(self):
        # Prefer using os.getenv for security
        openai.api_key = os.getenv('OPENAI_API_KEY', "YOUR_API_KEY")  
        if not openai.api_key:
            print("DEBUG: OpenAI API key not found!")
            exit()
        self.engine = "gpt-4"
        self.token_count = 0

    def ask(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.engine,
            messages=[{"role": "user", "content": prompt}]
        )
        self.token_count += response['usage']['total_tokens']
        return response['choices'][0]['message']['content'].strip()

def extract_content_between_markers(response, start_marker, end_marker):
    start_index = response.find(start_marker) + len(start_marker)
    end_index = response.find(end_marker, start_index)
    return response[start_index:end_index].strip()

def create_file_structure(base_path, structure):
    for key, value in structure.items():
        new_path = os.path.join(base_path, key)
        # If the value is an empty dictionary, treat it as a file
        if isinstance(value, dict) and not value:
            open(new_path, 'a').close()
        # If the value is a non-empty dictionary, treat it as a directory
        elif isinstance(value, dict) and value:
            os.makedirs(new_path, exist_ok=True)
            create_file_structure(new_path, value)


def gather_file_structure(directory):
    file_structure = []
    for root, dirs, files in os.walk(directory):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        for file in files:
            if file.endswith((".js", ".html", ".css")):
                file_structure.append(os.path.join(root, file))
    return file_structure

def populate_script_file(file_path, helper):
    open(file_path, 'w').close()  # Clear the file
    preprompt = f"Write content for {os.path.basename(file_path)}"
    code = helper.ask(preprompt)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)

def trim_content(file_path):
    """Trim the content of the file to only include content within triple backticks."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract content within triple backticks
    match = re.search(r'```[\s\S]*?```', content)
    if match:
        trimmed_content = match.group(0).replace("```", "").strip()  # Remove the backticks
    else:
        trimmed_content = ""  # If no match, set content to empty
    
    # Write the trimmed content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(trimmed_content)

def main():
    chat_gpt = UnifiedChatGPTApiClient()
    software_description = input("Please describe your software idea: ")

    clarification_prompt = f"Given the software idea described as {software_description}, please seek clarification if needed, your questions should be formatted in a numbered list wrapped using back ticks like so: ``` ```."
    clarifications_raw = chat_gpt.ask(clarification_prompt)
    clarifications_content = extract_content_between_markers(clarifications_raw, "```", "```")
    clarifications = clarifications_content.split("\n")
    
    user_answers = {}
    for clarification in clarifications:
        answer = input(f"{clarification}\nAnswer: ")
        user_answers[clarification] = answer

    user_responses_string = "\n".join([f"{k}: {v}" for k, v in user_answers.items()])
    outline_prompt = f""" I want to create the following software:
    {software_description} |
    Based on the following details:
    {user_responses_string} |
    Generate a file structure for the given idea and clarifications, your structure must be in JSON to illustrate subdirectories and identify files based on the needs and capabilities of the application. the JSON code itself must be wrapped using asterisks like so *** ***.
    """
    outline_response = chat_gpt.ask(outline_prompt)
    print(outline_response)

    outline_content = extract_content_between_markers(outline_response, "***", "***")
    outline = json.loads(outline_content)

    with open("outline.json", "w") as file:
        json.dump(outline, file, indent=4)
    print("Outline written to 'outline.json'!")

    normalized_software_description = software_description.replace(" ", "_")
    base_path = os.path.join(os.getcwd(), normalized_software_description)
    create_file_structure(base_path, outline)
    print(f"Directory structure created at: {base_path}")

    # Now, populate and trim the files based on the created structure
    file_structure = gather_file_structure(base_path)
    for file_path in file_structure:
        print(f"Populating {file_path}...")
        populate_script_file(file_path, chat_gpt)
    # After populating all files, trim the content
    for file_path in file_structure:
        print(f"Trimming content in {file_path}...")
        trim_content(file_path)


if __name__ == "__main__":
    main()