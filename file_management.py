import os
from pathlib import Path

def save_readme(content, repo_path, filename="README.md"):
    """
    Saves the generated README content to the specified repository path.
    
    :param content: String containing the README content
    :param repo_path: Path to the repository where the README should be saved
    :param filename: Name of the file to save (default is README.md)
    :return: True if successful, False otherwise
    """
    try:
        # Ensure the repo_path is a Path object
        repo_path = Path(repo_path)
        
        # Create the full file path
        file_path = repo_path / filename
        
        # Ensure the directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the content to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"README successfully saved to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving README: {str(e)}")
        return False