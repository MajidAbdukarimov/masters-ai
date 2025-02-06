import openai
import os

# Set your OpenAI API key
openai.api_key = "***"  # Replace with your actual API key

# Path to the transcript file
file_path = "lesson-1-transcript.txt"

# Read the transcript file
try:
    with open(file_path, "r", encoding="utf-8") as file:
        transcript_content = file.read()
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()

# Optimized prompt
prompt = "Generate a structured HTML blog post summarizing the following transcript:"

def generate_html_document(chunk, model="gpt-4", max_tokens=2000, temperature=0.7):
    """Generates an HTML document using OpenAI API."""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": "You are an expert in web content generation."},
                      {"role": "user", "content": prompt + chunk}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response['choices'][0]['message']['content']
    except openai.OpenAIError as e:
        return f"An error occurred: {e}"

# Split the transcript content into chunks if it's too long
chunk_size = 15000  # Adjust this based on the length of your transcript
chunks = [transcript_content[i:i + chunk_size] for i in range(0, len(transcript_content), chunk_size)]

# Initialize the HTML content
html_content = ""

# Generate HTML for each chunk
for i, chunk in enumerate(chunks):
    print(f"Generating HTML for chunk {i+1} of {len(chunks)}...")
    html_chunk = generate_html_document(chunk)
    html_content += html_chunk + "\n"

# Save the generated HTML content
output_file = "lecture_summary.html"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Blog post successfully generated and saved as '{output_file}'")
