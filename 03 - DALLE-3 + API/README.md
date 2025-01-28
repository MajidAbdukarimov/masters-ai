Image Generator Tool

Welcome to the Image Generator Tool, a Python-based script designed to generate images in various artistic styles using OpenAI's DALL·E API. Below is a guide on how to set up, run, and use this tool effectively.

Features

Generate images based on your textual prompts.

Supports multiple artistic styles, including:

Abstract Art

Realism

Cartoon Style

Impressionism

Surrealism

Cyberpunk

Steampunk

Pixel Art

Watercolor Painting

Saves image URLs locally in the generated_images folder.

Prerequisites

To use this tool, you need:

Python 3.8 or higher installed on your system.

An OpenAI API key.

dotenv and openai Python libraries installed.

Install the required libraries using:

pip install openai python-dotenv

Installation

Clone or download this repository.

Navigate to the project folder.

Create a .env file in the root directory and add your OpenAI API key:

OPENAI_API_KEY=your_api_key_here

Usage

Run the script using the command:

python image_generator.py

Enter a prompt for image generation when prompted. For example:

Enter a prompt for image generation: chess desk with neon lights and glass figures

The tool will generate images in the specified styles and save their URLs in the generated_images folder.

Output Example

For the prompt "chess desk with neon lights and glass figures", the following images are generated:

Abstract Art



Realism



Cartoon Style



Impressionism



Surrealism



Cyberpunk



Steampunk



Pixel Art



Note: Images in "Watercolor Painting" style might fail to generate due to API rate limits. Ensure compliance with OpenAI's rate limits to avoid errors.

Error Handling

If the script encounters errors (e.g., API rate limits):

Check your API usage and wait for the limit to reset.

Retry generating the failed images.

Folder Structure

image_generator.py: Main script for generating images.

generated_images/: Folder containing text files with image URLs.

License

This project is open-sourced under the MIT License. Feel free to modify and distribute it as needed.

Enjoy creating amazing visuals with the Image Generator Tool!
