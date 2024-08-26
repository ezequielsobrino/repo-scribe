import os
import fnmatch

def get_directory_info(dir_path, include_project_structure=True, include_file_contents=True, exclude_patterns=None, log_path=None):
    """
    Retrieves information from a local directory.

    Args:
        dir_path (str): Path to the local directory.
        include_project_structure (bool): Include project structure.
        include_file_contents (bool): Include file contents.
        exclude_patterns (list): Additional patterns to exclude.
        log_path (str): Optional path to save the log.

    Returns:
        str: Formatted directory information.
    """
    try:
        dir_name = os.path.basename(dir_path)
        
        output = [f"Directory Name: {dir_name}"]

        if include_project_structure:
            project_structure = get_project_structure(dir_path, exclude_patterns)
            output.append("\nProject Structure:")
            output.append(project_structure)

        if include_file_contents:
            file_contents = get_file_contents(dir_path, exclude_patterns)
            output.append("\nFile Contents:")
            output.append(file_contents)

        result = "\n".join(output)
        
        if log_path:
            with open(log_path, 'w', encoding='utf-8') as file:
                file.write(result)

        return result

    except Exception as e:
        # Log the exception or perform other actions
        # Re-throw the exception to be handled elsewhere
        raise Exception(f"Error retrieving directory information: {str(e)}")

def get_project_structure(dir_path, exclude_patterns=None):
    """
    Retrieves the project structure, excluding specified patterns for both files and directories.
    """
    exclude_patterns = exclude_patterns or []
    structure = []

    for root, dirs, files in os.walk(dir_path, topdown=True):
        # Create relative path
        rel_path = os.path.relpath(root, dir_path)
        level = rel_path.count(os.sep)
        indent = ' ' * 4 * level
        subindent = ' ' * 4 * (level + 1)

        # Check if the current directory should be excluded
        if any(fnmatch.fnmatch(os.path.basename(root), pattern) for pattern in exclude_patterns):
            dirs[:] = []  # Don't recurse into this directory
            continue  # Skip to the next iteration

        # Add current directory to structure
        if rel_path != '.':
            structure.append(f"{indent}{os.path.basename(root)}/")

        # Filter and sort files
        files = [f for f in files if not any(fnmatch.fnmatch(f, pattern) for pattern in exclude_patterns)]
        files.sort()

        # Add files to structure
        for f in files:
            structure.append(f"{subindent}{f}")

        # Filter directories in-place
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in exclude_patterns)]
        dirs.sort()

    return '\n'.join(structure)

def get_file_contents(dir_path, exclude_patterns=None):
    """
    Retrieves the contents of files, excluding patterns.
    """
    exclude_patterns = exclude_patterns or []
    contents = []
    for root, dirs, files in os.walk(dir_path):
        # Immediate exclusion for directories
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in exclude_patterns)]
        
        for file in files:
            # Exclude files based on patterns
            if not any(fnmatch.fnmatch(file, pattern) for pattern in exclude_patterns):
                relative_path = os.path.relpath(os.path.join(root, file), dir_path)
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                contents.append(f"\nFile: {relative_path}\n{file_content}")
    return "\n".join(contents)