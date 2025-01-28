# Employee Data Query Agent

This project creates an SQLite database with sample employee data and provides an agent that can answer specific queries about employees, such as listing employees in a department or querying the salary of a specific employee.

## Features

- **SQLite Database**: Stores employee data in a local SQLite database (`employee_data.db`).
- **Agent**: A simple agent that answers questions using SQL queries based on the data stored in the SQLite database.
- **Sample Data**: Pre-populated sample employee data.

## Technologies Used

- **Python 3.x**: The project is written in Python.
- **SQLite**: A lightweight, serverless SQL database used to store employee data.
- **SQL Queries**: Used to fetch and manipulate data from the database.

## How It Works

1. **Database Setup**: The program creates an SQLite database file named `employee_data.db` and populates it with a sample table `employees` that contains employee names, departments, and salaries.
2. **Agent**: The agent is capable of processing two types of questions:
    - **Department Query**: List employees from a specific department (e.g., "Who is in the Engineering department?").
    - **Salary Query**: Retrieve the salary of a specific employee (e.g., "What is the salary of Alice Johnson?").
3. **Execution**: The agent responds to questions using SQL queries against the database and returns the results.

## Requirements

- Python 3.x
- SQLite (comes pre-installed with Python)

## Setup and Usage

1. **Clone the Repository**: 
   Clone the project repository to your local machine.
   ```bash
