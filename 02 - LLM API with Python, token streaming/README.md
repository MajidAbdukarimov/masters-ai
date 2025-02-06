# Blog Post Generator using OpenAI GPT-4

This project demonstrates how to use OpenAI's GPT-4 API to generate an HTML blog post from a transcript file. The code reads the transcript, breaks it into smaller chunks, and sends them to the GPT-4 model to summarize and format them into an HTML blog post.

## Features

- **Chunking Large Files:** Handles large transcripts by splitting them into manageable chunks, avoiding token limits.
- **HTML Output:** Generates a structured HTML document summarizing the content of the transcript.
- **Error Handling:** Includes error handling for missing files or API issues.

## Requirements

- Python 3.7+
- OpenAI Python package
- A valid OpenAI API key

## Installation

1. **Clone this repository:**
    ```bash
    git clone https://github.com/yourusername/openai-blog-post-generator.git
    cd openai-blog-post-generator
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set your OpenAI API key:**
    - You can set the API key by adding it directly in the script:
      ```python
      openai.api_key = "your-api-key-here"
      ```
    - Or set the `OPENAI_API_KEY` environment variable:
      ```bash
      export OPENAI_API_KEY="your-api-key-here"  # Linux or macOS
      set OPENAI_API_KEY="your-api-key-here"  # Windows
      ```

## Usage

1. **Prepare your transcript file**: Ensure the transcript is saved as `transcript.txt` in the project directory. If your file has a different name, adjust the `file_path` in the script.

2. **Run the script**:
    ```bash
    python main.py
    ```

3. **Check the output**: Once the script finishes, an HTML file named `lecture_summary.html` will be generated in the project directory containing the summary of the transcript.

## Code Explanation

### 1. **Reading the Transcript**

The script reads the content of the transcript file (`transcript.txt`). If the file is not found, it will output an error.

### 2. **Chunking the Transcript**

If the transcript is too large (more than the token limit), the script breaks it down into smaller chunks. The chunk size is defined by the `chunk_size` variable.

### 3. **Generating the HTML Blog Post**

The code uses OpenAI's GPT-4 model via the `openai.ChatCompletion.create` API to generate a structured HTML blog post for each chunk. The prompt instructs GPT-4 to summarize the transcript into an HTML blog format.

### 4. **Saving the HTML Output**

The generated HTML content from each chunk is concatenated, and the complete HTML blog post is saved in `lecture_summary.html`.

## Error Handling

The script includes basic error handling for:
- Missing transcript file (`FileNotFoundError`).
- OpenAI API errors (`openai.OpenAIError`).

## Customization

- **Prompt Customization:** Modify the `prompt` variable to change how the blog post is generated.
- **Chunk Size:** Adjust the `chunk_size` if the input transcript is very large.

## Limitations

- **Token Limits:** The code handles large transcripts by chunking them. However, if the token limit is exceeded per chunk (due to output length), further adjustments may be necessary.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
