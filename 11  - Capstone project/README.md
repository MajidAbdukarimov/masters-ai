# Installation Instructions

Embark on your journey into our project with ease. Follow the steps below to set up your environment and begin exploring the world of generative AI in action.

---

## Prerequisites

Before you start, ensure you have the following:

- **Python 3.8+**: Our project is compatible with Python 3.8 and later.
- **pip**: The Python package installer.
- **Virtual Environment (Recommended)**: Isolate your project dependencies for a clean setup.

---

## Step 1: Clone the Repository

Clone the project repository from GitHub:

```sh
git clone https://github.com/your-username/your-project.git
cd your-project
```

---

## Step 2: Create and Activate a Virtual Environment

It is recommended to use a virtual environment:

```sh
python -m venv venv
```

Activate the virtual environment:

- **On macOS/Linux:**

  ```sh
  source venv/bin/activate
  ```

- **On Windows:**

  ```sh
  venv\Scripts\activate
  ```

---

## Step 3: Install Dependencies

Install the required packages using the provided `requirements.txt`:

```sh
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

Create a `.env` file in the root directory of the project. Populate it with the necessary environment variables:

```sh
OPENAI_API_KEY=your_openai_api_key_here
SENDER_EMAIL=your_sender_email@example.com
EMAIL_PASSWORD=your_email_password
DATABASE_URL=your_database_url_or_path
```

📌 **Note:** Make sure to add `.env` to your `.gitignore` to protect sensitive data.

---

## Step 5: Run the Application

Start the application using Streamlit:

```sh
streamlit run main.py
```

Your browser should automatically open a new tab with the application interface. If not, follow the URL provided in the terminal output.

---

## Troubleshooting

- **Virtual Environment Issues:** Ensure that the virtual environment is activated before installing dependencies.
- **Dependency Errors:** Double-check that all dependencies are correctly installed. Use `pip list` to confirm.
- **Environment Variables:** Verify that the `.env` file is in the correct location and contains the correct values.
- **API Key and Credits:** Ensure your OpenAI API key is valid and that your account has sufficient funds for API usage.
