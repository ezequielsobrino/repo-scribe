import os
from groq import Groq
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar el cliente de Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Definir secciones por defecto para el README
DEFAULT_SECTIONS = """
1. Project Name: The name of the project.
2. Brief Description: A concise overview of the project's purpose and objectives.
3. Main Features: A comprehensive list of the primary features and functionalities.
4. Prerequisites: Detailed requirements needed to run or develop the project (e.g., software versions, dependencies).
5. Installation: Step-by-step instructions for installing and configuring the project, including any environment setup.
6. Usage: Detailed instructions on how to use the project, including command-line arguments or configuration options.
7. Examples: Concrete examples and use cases demonstrating how to utilize the project's features.
8. Project Structure: A detailed description of the folder structure and key files, including their purpose and organization.
9. API Reference: Detailed API documentation, including endpoints, request/response formats, and authentication methods.
10. How to Contribute: Guidelines and best practices for contributing to the project, including code standards and pull request procedures.
11. Troubleshooting: Common issues and their resolutions to help users resolve potential problems.
12. Changelog: A log of notable changes, improvements, and bug fixes in the project.
13. License: Information about the project's licensing terms and conditions.
14. Contact: How to get in touch with the project maintainers for support or inquiries.
"""

def generate_readme_content(repo_info, sections=None):
    """
    Generates a comprehensive README.md for a project using the Groq API.

    :param repo_info: String containing detailed repository information.
    :param sections: String with numbered sections and their descriptions (optional).
    :return: Generated README content as a string.
    """
    if sections is None:
        sections = DEFAULT_SECTIONS
    
    prompt = f"""
    Generate an expert-level README.md for a project based on the following repository information:

    {repo_info}

    The README should include the following sections with their respective descriptions:
    {sections}

    Use Markdown for formatting. Ensure that the content is detailed, clear, and informative, providing all necessary information for an advanced user or developer.
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
