import os
from generate_readme_content import generate_readme_content
from file_management import save_readme
from repo_info_extractor import get_directory_info

def main(repo_path, include_project_structure, include_file_contents, exclude_patterns, log_path):
    # Validate the repository path
    if not os.path.isdir(repo_path):
        print(f"Error: The path '{repo_path}' is not a valid directory.")
        return
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(base_path, 'outputs')
    full_log_path = os.path.join(output_path, log_path)

    # Extract directory information
    print("Extracting directory information...")
    repo_info = get_directory_info(
        dir_path=repo_path,
        include_project_structure=include_project_structure,
        include_file_contents=include_file_contents,
        exclude_patterns=exclude_patterns,
        log_path=full_log_path
    )

    # Generate README content
    print("Generating README content...")
    readme_content = generate_readme_content(repo_info)

    # Save the README file
    print("Saving README file...")
    if save_readme(readme_content, repo_path):
        print("README.md has been successfully generated and saved.")
    else:
        print("Failed to save README.md.")

if __name__ == "__main__":
    # Get the repository path from the user
    repo_path = input("Enter the path to your repository: ").strip()

    # Example usage:
    main(
        repo_path=repo_path,
        include_project_structure=True,
        include_file_contents=True,
        exclude_patterns=['*.pyc', '__pycache__'],
        log_path='directory_info.log'  # Relative path within the output folder
    )

