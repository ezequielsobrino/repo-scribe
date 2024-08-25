import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DEFAULT_SECTIONS = """
1. Project name: The name of the project
2. Brief description: A short and clear description of the project's purpose
3. Main features: List of the project's key features
4. Prerequisites: Requirements needed to use the project (software versions, etc.)
5. Installation: Steps to install and set up the project
6. Usage: Basic instructions on how to use the project
7. Examples: Concrete examples of project usage
8. Project structure: Description of the folder structure and main files
9. How to contribute: Guide for other developers to contribute to the project
10. License: Information about the project's license
"""

def generate_readme_content(repo_info, sections=None):
    """
    Generates README content using the Groq API.
    
    :param repo_info: String containing repository information
    :param sections: String with numbered sections and their descriptions (optional)
    :return: Generated README content
    """
    if sections is None:
        sections = DEFAULT_SECTIONS
    
    prompt = f"""
    Generate a README.md for an API project based on the following repository information:
    
    {repo_info}
    
    The README should include the following sections, with their respective descriptions:
    {sections}
    
    Use Markdown to format the README. Be concise but informative, following the description for each section.
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