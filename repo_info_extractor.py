import os
import fnmatch

def get_directory_info(dir_path, include_commit_history=False, include_project_structure=True, include_file_contents=True, exclude_patterns=None, log_path=None):
    """
    Retrieves information from a local directory.

    Args:
        dir_path (str): Path to the local directory.
        include_commit_history (bool): Include full commit history (not applicable here, kept for interface consistency).
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
            with open(log_path, 'w') as file:
                file.write(result)

        return result

    except Exception as e:
        return f"Error retrieving directory information: {str(e)}"

def get_project_structure(dir_path, exclude_patterns=None):
    """
    Retrieves the project structure, excluding patterns.
    """
    exclude_patterns = exclude_patterns or []
    structure = []
    for root, dirs, files in os.walk(dir_path):
        # Exclude directories and files based on patterns
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in exclude_patterns)]
        for file in files:
            if not any(fnmatch.fnmatch(file, pattern) for pattern in exclude_patterns):
                relative_path = os.path.relpath(os.path.join(root, file), dir_path)
                structure.append(relative_path)
    return "\n".join(structure)

def get_file_contents(dir_path, exclude_patterns=None):
    """
    Retrieves the contents of files, excluding patterns.
    """
    exclude_patterns = exclude_patterns or []
    contents = []
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in exclude_patterns)]
        for file in files:
            if not any(fnmatch.fnmatch(file, pattern) for pattern in exclude_patterns):
                relative_path = os.path.relpath(os.path.join(root, file), dir_path)
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                contents.append(f"\nFile: {relative_path}\n{file_content}")
    return "\n".join(contents)


