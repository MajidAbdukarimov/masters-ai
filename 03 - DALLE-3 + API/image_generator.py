import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key. Please set it in the .env file.")

openai.api_key = OPENAI_API_KEY

# Predefined styles for image generation
STYLES = [
    "abstract art",
    "realism",
    "cartoon style",
    "impressionism",
    "surrealism",
    "cyberpunk",
    "steampunk",
    "pixel art",
    "watercolor painting"
]

# Output folder for images
OUTPUT_FOLDER = "generated_images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to generate an image via DALL·E API
def generate_image(prompt, style, index):
    try:
        print(f"Generating image {index + 1} in {style}...")
        response = openai.Image.create(
            prompt=f"{prompt} in {style}",
            n=1,  # Number of images to generate
            size="512x512"  # Image resolution
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        print(f"Error generating image {index + 1}: {e}")
        return None

# Main function
def main():
    # Get user input
    user_prompt = input("Enter a prompt for image generation: ").strip()

    # Generate images in different styles
    for index, style in enumerate(STYLES):
        image_url = generate_image(user_prompt, style, index)
        if image_url:
            # Save the image URL as a text file or download the image (if needed)
            output_path = os.path.join(OUTPUT_FOLDER, f"image_{index + 1}_{style.replace(' ', '_')}.txt")
            with open(output_path, "w") as file:
                file.write(image_url)
            print(f"Image {index + 1} ({style}) URL saved to {output_path}")
        else:
            print(f"Failed to generate image {index + 1} in {style}.")

if __name__ == "__main__":
    main()
