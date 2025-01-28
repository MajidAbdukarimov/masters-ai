import sqlite3

# Function to connect to the database and execute SQL queries
def query_db(query, params=()):
    # Connect to the database
    conn = sqlite3.connect('employee_data.db')
    cursor = conn.cursor()

    # Execute the query with parameters
    cursor.execute(query, params)
    result = cursor.fetchall()

    # Close the connection
    conn.close()

    return result

# Agent function to interpret and answer questions
def agent(question):
    # Basic parsing of the question to build SQL query
    if "Engineering" in question:
        return query_db("SELECT name FROM employees WHERE department = 'Engineering'")
    elif "salary of" in question:
        # Extract the name after "salary of" and strip any extra spaces
        name = question.split("salary of")[-1].strip()

        # Query the database using the exact name, and sanitize the name
        result = query_db("SELECT salary FROM employees WHERE name = ?", (name,))

        # Check if result is empty and return a message
        if result:
            return result
        else:
            return f"Salary for {name} not found."
    else:
        return "I don't understand the question."

# Create the SQLite database and insert sample data
def setup_db():
    # Connect to SQLite (or create it)
    conn = sqlite3.connect('employee_data.db')
    cursor = conn.cursor()

    # Create a sample table for employees
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            salary REAL
        )
    ''')

    # Insert sample data using parameterized query
    cursor.executemany('''
        INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)
    ''', [
        ('John Doe', 'Engineering', 80000),
        ('Jane Smith', 'Marketing', 75000),
        ('Alice Johnson', 'Engineering', 95000),
        ('Bob Brown', 'HR', 70000)
    ])

    # Commit and close connection
    conn.commit()
    conn.close()

# Main function to run the application
def main():
    # Set up the database and insert sample data
    setup_db()

    # Test the agent with sample questions
    question_1 = "Who is in the Engineering department?"
    print(f"Question: {question_1}")
    answer_1 = agent(question_1)
    print(f"Answer: {answer_1}")

    question_2 = "What is the salary of Alice Johnson?"
    print(f"\nQuestion: {question_2}")
    answer_2 = agent(question_2)
    print(f"Answer: {answer_2}")

    question_3 = "What is the salary of John Doe?"
    print(f"\nQuestion: {question_3}")
    answer_3 = agent(question_3)
    print(f"Answer: {answer_3}")

# Run the main function
if __name__ == "__main__":
    main()
