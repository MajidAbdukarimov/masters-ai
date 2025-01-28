import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_blog_post(transcript):
    """
    Generates a blog post based on a given transcript using OpenAI's updated API.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" for higher quality output
            messages=[
                {"role": "system", "content": "You are an assistant that generates blog posts."},
                {"role": "user", "content": f"Create a detailed blog post based on the following transcript:\n{transcript}\n\nEnsure the output is in Markdown format."}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error generating blog post: {e}")
        return None

if __name__ == "__main__":
    transcript = "Example transcript content here."
    blog_post = generate_blog_post(transcript)
    if blog_post:
        print(blog_post)
    else:
        print("Failed to generate the blog post.")
