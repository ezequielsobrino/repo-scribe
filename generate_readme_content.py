import os
import time
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

MAX_TOKENS = 8000
TOKENS_PER_MINUTE = 131072
REQUESTS_PER_MINUTE = 100

def split_repo_info(repo_info, max_chunk_size=8000):
    """Split repo_info into smaller chunks."""
    words = repo_info.split()
    chunks = []
    current_chunk = []
    current_size = 0

    for word in words:
        if current_size + len(word) > max_chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_size = len(word)
        else:
            current_chunk.append(word)
            current_size += len(word) + 1  # +1 for space

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def extract_notes_from_chunk(chunk, sections, log_file="D:\\repos\\repo-scribe\\response_log.txt"):
    """Extract important notes from a single chunk and log the response."""
    prompt = f"""
    Extract important notes for a README.md from the following repository information:
    
    {chunk}
    
    Focus on the key points relevant to these sections:
    {sections}
    
    The notes should be concise and capture essential details for each relevant section.
    """
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.1-70b-versatile",
        max_tokens=MAX_TOKENS,
        temperature=0.5,
    )
    
    content = response.choices[0].message.content

    # Log the response to a file
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(content + "\n\n")
    
    return content

def calculate_remaining_time(total_chunks, processed_chunks, time_per_request):
    """Calculate the remaining time to complete all requests."""
    remaining_chunks = total_chunks - processed_chunks
    remaining_time = remaining_chunks * time_per_request
    
    return remaining_time

def generate_readme_content(repo_info, sections=None):
    """
    Generates README content using the Groq API, handling large repositories.
    
    :param repo_info: String containing repository information
    :param sections: String with numbered sections and their descriptions (optional)
    :return: Generated README content
    """
    if sections is None:
        sections = DEFAULT_SECTIONS
    
    chunks = split_repo_info(repo_info)
    notes = []
    tokens_used = 0
    requests_made = 0

    print(f"Processing {len(chunks)} chunks of repository information...")

    for i, chunk in enumerate(chunks):
        # Check if we're approaching rate limits
        if tokens_used + MAX_TOKENS > TOKENS_PER_MINUTE or requests_made + 1 > REQUESTS_PER_MINUTE:
            wait_time = 60 - (time.time() % 60)  # Time until the next minute
            print(f"Approaching rate limits. Waiting for {wait_time:.2f} seconds...")
            time.sleep(wait_time)
            tokens_used = 0
            requests_made = 0

        print(f"Extracting notes for chunk {i+1}/{len(chunks)}...")
        chunk_notes = extract_notes_from_chunk(chunk, sections)
        notes.append(chunk_notes)

        tokens_used += MAX_TOKENS  # Assume worst case
        requests_made += 1

        # Provide feedback on progress
        print(f"Progress: {((i+1)/len(chunks))*100:.2f}% complete")

        # Calculate and print remaining time
        time_per_request = 60 / REQUESTS_PER_MINUTE  # Time per request in seconds
        remaining_time = calculate_remaining_time(len(chunks), i + 1, time_per_request)
        remaining_minutes = int(remaining_time // 60)
        remaining_seconds = int(remaining_time % 60)
        print(f"Estimated remaining time: {remaining_minutes} minutes and {remaining_seconds} seconds.")

    # Combine all notes to create the README content
    all_notes = "\n\n".join(notes)

    # Generate the final README content based on notes
    readme_prompt = f"""
    Based on the following notes, generate a coherent and comprehensive README.md:

    {all_notes}
    
    Follow the structure of the sections provided earlier.
    """

    print("Generating final README content...")
    final_readme = extract_notes_from_chunk(readme_prompt, sections)

    return final_readme
