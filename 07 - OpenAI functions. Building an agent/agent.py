import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to connect to the database and execute SQL queries
def query_db(query, params=()):
    conn = sqlite3.connect('employee_data.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Agent function to interpret and answer questions
def agent(question):
    if "Engineering" in question:
        return query_db("SELECT name FROM employees WHERE department = 'Engineering'")
    elif "salary of" in question:
        name = question.split("salary of")[-1].strip()
        result = query_db("SELECT salary FROM employees WHERE name = ?", (name,))
        if result:
            return result
        else:
            return f"Salary for {name} not found."
    else:
        return "I don't understand the question."

# Function to handle the button click event
def on_query_button_click():
    question = question_entry.get()
    if question:
        answer = agent(question)
        if isinstance(answer, list):
            answer_text.set("\n".join([str(item[0]) for item in answer]))
        else:
            answer_text.set(answer)
    else:
        messagebox.showerror("Input Error", "Please enter a question.")

# Create the main window
root = tk.Tk()
root.title("Employee Query Agent")

# Set the window size
root.geometry("500x300")

# Create widgets
question_label = tk.Label(root, text="Enter your question:")
question_label.pack(pady=10)

question_entry = tk.Entry(root, width=50)
question_entry.pack(pady=10)

query_button = tk.Button(root, text="Ask", command=on_query_button_click)
query_button.pack(pady=10)

answer_label = tk.Label(root, text="Answer:")
answer_label.pack(pady=10)

answer_text = tk.StringVar()
answer_display = tk.Label(root, textvariable=answer_text, width=50, height=5, relief="sunken", anchor="nw", justify="left")
answer_display.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
