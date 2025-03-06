import os
import openai
import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import logging
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
from conversation import Conversation
from email_handler import send_email_notification

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"  # Ensure this model name is valid
DATABASE = "products_data.db"
USER_EMAIL = "abdumajid_abdukarimov@mail.ru"  # Ensure defined
ADMIN_EMAIL = "mjdabdkrmv@gmail.com"  # Ensure defined

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, model=MODEL):
    """Send a request to the ChatGPT API with optional function calling."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})

    logging.info(f"Sending request to OpenAI API: {json_data}")
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        response.raise_for_status()  # Raise an error for HTTP error statuses
        return response
    except Exception as e:
        logging.error(f"Request error: {e}\nRequest data: {json_data}")
        raise Exception(f"Failed to get ChatCompletion response: {e}")

def ask_database(conn, query):
    """Execute an SQL query on a SQLite database."""
    try:
        results = conn.execute(query).fetchall()
        return results
    except Exception as e:
        raise Exception(f"SQL error: {e}")

def plot_price_trend(product_code, conn):
    """Plot the price trend for a product."""
    query = f"""
    SELECT month, price
    FROM products
    WHERE product_code = '{product_code}'
    ORDER BY month;
    """
    data = pd.read_sql(query, conn)
    
    if data.empty:
        st.info("No data available for plotting.")
        return None

    data['month'] = pd.to_datetime(data['month'], format='%m-%Y', errors='coerce')  # Format: MM-YYYY
    if data['month'].isnull().any():
        st.error("Date parsing error. Check the 'month' field format.")
        return None

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='month', y='price', data=data, marker='o')
    plt.title(f"Price Trend for Product Code {product_code}")
    plt.xlabel('Month')
    plt.ylabel('Price ($)')
    plt.grid(True)
    st.pyplot(plt)

def send_error_email(error_message):
    """Send an email notification about an error."""
    subject = "Error in Processing Query"
    body = f"An error occurred while processing the query:\n\n{error_message}"
    send_email_notification(user_email=USER_EMAIL, admin_email=ADMIN_EMAIL, subject=subject, body=body)

def chat_completion_with_function_execution(messages, functions=None):
    """
    Call the ChatCompletion API and execute the function if needed.
    Returns the final text response.
    """
    try:
        response = chat_completion_request(messages, functions)
        response_json = response.json()
        full_choice = response_json["choices"][0]
        full_message = full_choice["message"]
        # If API requested a function call
        if full_choice.get("finish_reason") == "function_call":
            st.write("Function call requested, executing...")
            return call_function(messages, full_choice)
        else:
            return full_message.get("content", "").strip()
    except Exception as e:
        send_error_email(str(e))
        st.error(f"Error occurred: {e}")
        return f"Error: {e}"

def call_function(messages, full_choice):
    """Execute the function call if required and return the final text response."""
    function_call = full_choice["message"].get("function_call", {})
    if function_call.get("name") == "ask_database":
        try:
            # Convert arguments into a dictionary
            arguments = eval(function_call.get("arguments", "{}"))
            st.write(f"Executing SQL query: {arguments.get('query')}")
            conn = sqlite3.connect(DATABASE)
            results = ask_database(conn, arguments.get("query"))
            conn.close()
        except Exception as e:
            st.error(f"SQL execution error: {e}")
            send_error_email(f"Query failed: {e}")
            return f"Error executing query: {e}"
        messages.append({
            "role": "function", 
            "name": "ask_database", 
            "content": str(results)
        })
        try:
            followup_response = chat_completion_request(messages)
            followup_json = followup_response.json()
            return followup_json["choices"][0]["message"].get("content", "").strip()
        except Exception as e:
            st.error(f"Follow-up function call error: {e}")
            send_error_email(f"Follow-up function call failed: {e}")
            return f"Error in follow-up function call: {e}"
    else:
        st.error("Function not recognized")
        return "Error: Function not recognized"

# System message for the database assistant
agent_system_message = """You are DatabaseGPT, a helpful assistant who retrieves answers to user questions from the Database.
Provide as many details as possible to your users.
Begin!"""

if __name__ == '__main__':
    conversation = Conversation()
    conn = sqlite3.connect(DATABASE)

    # Database schema description
    database_schema_string = """
    Table: products
    Columns: id, product_code, product_name, category, color, capacity, price, monthly_sales, stock_remaining, segment, discount, country_of_origin, product_index, flag, month
    """

    functions = [
        {
            "name": "ask_database",
            "description": "Use this function to answer user questions about data. Output should be a fully formed SQL query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"""
                                SQL query extracting info to answer the user's question.
                                SQL should be written using this database schema:
                                {database_schema_string}
                                The query should be returned in plain text, not in JSON.
                                """,
                    }
                },
                "required": ["query"],
            },
        }
    ]

    conversation.add_message("system", agent_system_message)

    st.title("Database Query Assistant")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "query_input" not in st.session_state:
        st.session_state.query_input = ""

    role_backgrounds = {
        "user": "#DCF8C6", 
        "assistant": "#F1F1F1",  
        "function": "#F5F5F5",  
        "system": "#E6E6FA"  
    }

    # Display conversation messages
    for message in st.session_state["messages"]:
        background_color = role_backgrounds.get(message['role'], '#FFFFFF')
        alignment = 'right' if message['role'] == "user" else 'left'
        st.markdown(
            f"<div style='background-color:{background_color}; padding: 12px; border-radius: 8px; "
            f"box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1); margin-bottom: 4px; text-align:{alignment};'>"
            f"<b style='color: black;'>{message['role'].capitalize()}:</b><br>"
            f"<span style='color: black;'>{message['content']}</span></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        query_input = st.text_input("Query input", key="query_input", label_visibility="collapsed", placeholder="Enter your query here...")
    with col2:
        submit_button = st.button("Send Query")

    if submit_button and query_input:
        if query_input not in [msg['content'] for msg in st.session_state["messages"]]:
            conversation.add_message("user", query_input)
            st.session_state["messages"].append({"role": "user", "content": query_input})

            # Send email notification for new query
            send_email_notification(
                user_email=USER_EMAIL,
                admin_email=ADMIN_EMAIL,
                subject="New Query Received",
                body=f"User with email {USER_EMAIL} has asked a query: '{query_input}'"
            )

            # Get response from the assistant
            assistant_response = chat_completion_with_function_execution(conversation.messages, functions=functions)
            conversation.add_message("assistant", assistant_response)
            st.session_state["messages"].append({"role": "assistant", "content": assistant_response})

            # If query contains "product_code", plot the price trend
            if "product_code" in query_input.lower():
                plot_price_trend(query_input, conn)
        else:
            st.warning("You've already asked this query.")