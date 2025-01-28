# Employee Query Agent with UI

This project adds a graphical user interface (UI) to the Employee Query Agent, allowing users to ask questions about employees stored in an SQLite database through a simple window.

## Features

- **UI for Queries**: A window where users can enter questions about employees (e.g., "Who is in the Engineering department?").
- **Database Integration**: Queries are processed against an SQLite database (`employee_data.db`), and answers are shown on the UI.
- **Simple Interface**: A clean and easy-to-use interface using Python's `Tkinter` library.

## How It Works

1. **Database Setup**: The agent uses data stored in an SQLite database (`employee_data.db`), which contains employee names, departments, and salaries.
2. **Agent Functionality**: The agent processes user queries (e.g., "Who is in the Engineering department?") and fetches the relevant data from the database.
3. **UI Interaction**: The user types a question in the provided text entry field, clicks the "Ask" button, and sees the result below.

## Technologies Used

- **Python 3.x**: The project is written in Python.
- **Tkinter**: Used for the graphical user interface.
- **SQLite**: Stores employee data.

## Setup and Usage

1. **Clone the Repository**:
   Clone the project repository to your local machine.
   ```bash
   git clone <repository-url>
