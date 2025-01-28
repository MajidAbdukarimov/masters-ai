# Image Generator Tool

Welcome to the **Image Generator Tool**, a Python-based script designed to generate images in various artistic styles using OpenAI's DALL·E API. Below is a guide on how to set up, run, and use this tool effectively.

---

### Image Generation Prompt:
*Prompt*: Chess desk with neon lights and glass figures.


## Features
- Generate images based on your textual prompts.
- Supports multiple artistic styles, including:
  - Abstract Art
    
  ![1 abstract art.png](./1.png)
  - Realism

    ![1 abstract art.png](./2.png)
  - Cartoon Style
    
    ![1 abstract art.png](./3.png)
  - Impressionism

       ![1 abstract art.png](./4.png)
  - Surrealism

       ![1 abstract art.png](./5.png)
  - Cyberpunk

      ![1 abstract art.png](./6.png)
  - Steampunk
    
      ![1 abstract art.png](./7.png)
  - Pixel Art

      ![1 abstract art.png](./8.png)
  - Watercolor Painting (Error)
  
- Saves image URLs locally in the `generated_images` folder.

---

## Prerequisites
To use this tool, you need:
1. Python 3.8 or higher installed on your system.
2. An OpenAI API key.
3. `dotenv` and `openai` Python libraries installed.

Install the required libraries using:
```bash
pip install openai python-dotenv
