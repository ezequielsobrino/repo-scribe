import os
import ast
import argparse
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def parse_repository(repo_path):
    """
    Analyzes the repository and extracts relevant information.
    """
    repo_info = {
        "name": os.path.basename(repo_path),
        "files": [],
        "classes": [],
        "functions": []
    }
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                repo_info["files"].append(file_path)
                
                with open(file_path, 'r') as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        repo_info["classes"].append(node.name)
                    elif isinstance(node, ast.FunctionDef):
                        repo_info["functions"].append(node.name)
    
    return repo_info

def generate_readme_content(repo_info):
    """
    Generates the README content using the Groq API.
    """
    prompt = f"""
    Generate a README.md for an API project based on the following information:
    
    Repository name: {repo_info['name']}
    Main files: {', '.join(repo_info['files'])}
    Main classes: {', '.join(repo_info['classes'])}
    Main functions: {', '.join(repo_info['functions'])}
    
    The README should include the following sections:
    1. Project name
    2. Brief description
    3. Main features
    4. Prerequisites
    5. Installation
    6. Usage
    7. Examples
    8. How to contribute
    9. License
    
    Use Markdown to format the README. Be concise but informative.
    """
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.1-70b-versatile",
        max_tokens=2048,
        temperature=0.5,
    )
    
    return response.choices[0].message.content

def main(repo_path):
    repo_info = parse_repository(repo_path)
    readme_content = generate_readme_content(repo_info)
    
    with open(os.path.join(repo_path, 'README.md'), 'w') as f:
        f.write(readme_content)
    
    print(f"README.md successfully generated in {repo_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a README.md for an API repository")
    parser.add_argument("repo_path", help="Path to the repository")
    args = parser.parse_args()
    
    main(args.repo_path)