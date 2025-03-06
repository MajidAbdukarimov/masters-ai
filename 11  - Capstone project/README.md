Database Query Assistant

This project implements a Database Query Assistant using OpenAI's GPT model and a SQLite database. The assistant helps users query a product database and generates responses based on the data. It supports sending queries, receiving responses, and visualizing data trends, such as price trends over time. Additionally, it includes features like error notification via email and detailed logging for better monitoring.

Features

Conversational Interface: Interact with the assistant to ask questions related to product data stored in a SQLite database.

Database Interaction: The assistant can run SQL queries on the database and return the results.

Data Visualization: Display price trends for products over time.

Email Notifications: Notifies admins about new user queries and errors via email.

Logging: Detailed logging of actions and errors, stored both in the console and in log files with rotation.

Streamlit UI: A simple, interactive user interface built using Streamlit.

Requirements

Python 3.12 or below

OpenAI API Key (for GPT model usage)

SQLite (for the product database)

Streamlit (for the UI)

Requests (for making HTTP requests)

Pandas, Matplotlib, Seaborn (for data processing and visualization)

Termcolor (for colored terminal output)

Tenacity (for retries and error handling)

Dotenv (for environment variable management)

Installation

Clone the repository:

bashCopygit clone https://github.com/your-repo/database-query-assistant.git

cd database-query-assistant

Install required dependencies:

bashCopypip install -r requirements.txt

Create a .env file in the root directory and add the following environment variables:

envCopyOPENAI\_API\_KEY=your\_openai\_api\_key

SENDER\_EMAIL=your\_email\_address

EMAIL\_PASSWORD=your\_email\_password

LOG\_FILE=path\_to\_log\_file

Set up your SQLite database:

Ensure your database (products\_data.db) contains a products table with the following schema:

id, product\_code, product\_name, category, color, capacity, price, monthly\_sales, stock\_remaining, segment, discount, country\_of\_origin, product\_index, flag, month


Run the application:

bashCopystreamlit run main.py


How It Works

User Interaction

The user enters a query via the Streamlit interface.

The assistant processes the query and checks if it requires interaction with the database.

If the query involves a product code, the assistant will fetch relevant data from the database and visualize it (e.g., a price trend).

The response is displayed to the user, and an email notification is sent to the admin.

Function Execution

The assistant can perform SQL queries on the database via the ask\_database function.

It also supports executing custom functions based on user input.

Error Handling

Errors are logged to the console and stored in log files.

If any error occurs (e.g., invalid queries, database connection issues), an email is sent to the admin to notify them of the issue.

Logging

All actions, including database queries, function calls, and errors, are logged.

Logs are stored both in the console and in a log file (app.log by default). Log rotation is enabled to manage file size.

Example Use Cases

Query a product's price trend:

Query: "What is the price trend for product code ABC123?"

Response: A graph showing the price trend over time for the specified product.

Get product details:

Query: "Tell me about the product with code XYZ789."

Response: Details about the product (e.g., name, category, price, etc.).

Notify about an error:

If an invalid SQL query is submitted, the system will send an email notification to the admin.

File Overview

main.py: Main entry point for running the application. It sets up the Streamlit UI and manages interactions with the database and the GPT model.

conversation.py: Manages the conversation history, adds messages, and saves the conversation to a file.

email\_handler.py: Sends email notifications to the admin for errors or new user queries.

logger.py: Sets up logging for the application, including file-based log rotation.

.env: Stores sensitive configuration information like API keys and email credentials.

Error Handling

The project includes mechanisms to handle errors gracefully:

API request errors: If the OpenAI API request fails, the system logs the error and sends an email notification to the admin.

Database errors: SQL query errors are caught, logged, and an email is sent to notify the admin.

Email notifications: The system sends emails to notify the admin about errors or new user queries.

Contributing

Fork the repository.

Create a new branch for your feature or bug fix.

Make your changes and commit them.

Push to your forked repository.

Open a pull request to the main repository.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Note: Please ensure to replace placeholders like your\_openai\_api\_key and your\_email\_address with actual values in your .env file.
