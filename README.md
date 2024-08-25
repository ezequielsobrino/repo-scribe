# repo-scribe
================

## Project Name
------------

repo-scribe is a Python-based tool designed to generate high-quality README files for GitHub repositories.

## Brief Description
-------------------

repo-scribe aims to simplify the process of creating and maintaining README files by automatically extracting relevant information from the repository and generating a well-structured Markdown file.

## Main Features
----------------

*   Automatic extraction of repository information
*   Generation of high-quality README files in Markdown format
*   Customizable content sections
*   Easy integration with existing repositories

## Prerequisites
----------------

*   Python 3.8+
*   Git

## Installation
--------------

To install repo-scribe, follow these steps:

1.  Clone the repository: `git clone https://github.com/ezequielsobrino/repo-scribe.git`
2.  Navigate to the repository directory: `cd repo-scribe`
3.  Install the required dependencies: `pip install -r requirements.txt`

## Usage
-----

To generate a README file for your repository, follow these steps:

1.  Run the `main.py` script: `python main.py`
2.  Enter the path to your repository when prompted
3.  The script will extract the necessary information and generate a README file in the repository directory

## Examples
---------

*   Generate a README file for a Python project: `python main.py /path/to/your/python/project`
*   Generate a README file for a JavaScript project: `python main.py /path/to/your/javascript/project`

## Project Structure
---------------------

The repository is organized into the following directories and files:

*   `extract_repo_info.py`: Script responsible for extracting repository information
*   `generate_readme_content.py`: Script responsible for generating README content
*   `file_management.py`: Script responsible for saving the README file
*   `main.py`: Main script that orchestrates the README generation process
*   `requirements.txt`: File containing the required dependencies
*   `LICENSE`: File containing the project's license information

## How to Contribute
----------------------

Contributions are welcome! To contribute to repo-scribe, follow these steps:

1.  Fork the repository: `git fork https://github.com/ezequielsobrino/repo-scribe.git`
2.  Create a new branch: `git branch feature/new-feature`
3.  Make changes and commit them: `git commit -m "Added new feature"`
4.  Push the changes to your fork: `git push origin feature/new-feature`
5.  Open a pull request: `git pull-request https://github.com/ezequielsobrino/repo-scribe.git`

## License
-------

repo-scribe is licensed under the MIT License. See the `LICENSE` file for more information.

Copyright (c) 2024 Ezequiel Sobrino

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.