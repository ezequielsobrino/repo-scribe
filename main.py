import os
from extract_repo_info import extract_repo_info
from generate_readme_content import generate_readme_content
from file_management import save_readme

def main():
    # Get the repository path from the user
    repo_path = input("Enter the path to your repository: ").strip()

    # Validate the repository path
    if not os.path.isdir(repo_path):
        print(f"Error: The path '{repo_path}' is not a valid directory.")
        return

    # Extract repository information
    print("Extracting repository information...")
    repo_info = extract_repo_info(repo_path, save_output=False)

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
    main()
    