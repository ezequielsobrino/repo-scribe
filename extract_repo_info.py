import os
import subprocess
import shlex
import fnmatch

def extract_repo_info(repo_path, save_output=False):
    def run_command(command):
        args = shlex.split(command)
        try:
            return subprocess.check_output(args, stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            return f"Error executing the command: {command}\nError output: {e.output}"

    def get_file_content(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                return file.read()
        except Exception as e:
            return f"Error reading the file: {str(e)}"

    def get_gitignore_patterns(repo_path):
        gitignore_path = os.path.join(repo_path, '.gitignore')
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return []

    def should_ignore(file_path, ignore_patterns):
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
        # Additional check for files and directories starting with '.'
        return os.path.basename(file_path).startswith('.')

    def get_directory_structure(startpath, ignore_patterns):
        tree = []
        for root, dirs, files in os.walk(startpath, topdown=True):
            dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_patterns)]  # Filter directories first
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            basename = os.path.basename(root)
            if not should_ignore(os.path.relpath(root, startpath), ignore_patterns):
                tree.append(f"{indent}{basename}/")
                subindent = ' ' * 4 * (level + 1)
                for f in files:
                    file_path = os.path.relpath(os.path.join(root, f), startpath)
                    if not should_ignore(file_path, ignore_patterns):
                        tree.append(f"{subindent}{f}")
        return '\n'.join(tree)

    repo_name = os.path.basename(repo_path)
    os.chdir(repo_path)

    ignore_patterns = get_gitignore_patterns(repo_path)
    project_structure = get_directory_structure(repo_path, ignore_patterns)
    files = run_command("git ls-files").splitlines()
    repo_url = run_command("git config --get remote.origin.url").strip()
    commit_history = run_command("git log --pretty=format:'%h - %an, %ad : %s' --date=short")

    output = [f"Repository Name: {repo_name}",
              f"Repository URL: {repo_url}\n",
              "Full Commit History:",
              commit_history,
              "\nProject Structure:",
              project_structure,
              "\nFile Contents:"]

    for file in files:
        if not should_ignore(file, ignore_patterns):
            if os.path.isfile(file):
                output.append(f"\nFile: {file}")
                output.append("=" * 50)
                content = get_file_content(file)
                output.append(content)

    output_str = "\n".join(output)
    if save_output:
        output_file = os.path.join(repo_path, 'repo_info_log.txt')
        with open(output_file, 'w') as f:
            f.write(output_str)
    return output_str
