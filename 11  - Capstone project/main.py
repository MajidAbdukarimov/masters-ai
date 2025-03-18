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
from email_handler import send_email_notification, send_query_notification, send_error_notification, send_assistant_response_notification
import json
from datetime import datetime

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Database Query Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"  # Ensure this model name is valid
DATABASE = "products_data.db"
USER_EMAIL = "abdumajid_abdukarimov@mail.ru"  # Ensure defined
ADMIN_EMAIL = "mjdabdkrmv@gmail.com"  # Ensure defined

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Starting application")

# Function to get product summary statistics
def get_product_summary(conn):
    try:
        # Total products
        total_products = conn.execute("SELECT COUNT(DISTINCT product_code) FROM products").fetchone()[0]
        
        # Average price
        avg_price = conn.execute("SELECT AVG(price) FROM products").fetchone()[0]
        
        # Total sales
        total_sales = conn.execute("SELECT SUM(monthly_sales) FROM products").fetchone()[0]
        
        # Average monthly sales per product
        avg_monthly_sales = conn.execute("SELECT AVG(monthly_sales) FROM products").fetchone()[0]
        
        # Top categories
        top_categories = conn.execute("""
            SELECT category, COUNT(*) as count 
            FROM products 
            GROUP BY category 
            ORDER BY count DESC 
            LIMIT 5
        """).fetchall()
        
        # Top countries of origin
        top_countries = conn.execute("""
            SELECT country_of_origin, COUNT(*) as count 
            FROM products 
            GROUP BY country_of_origin 
            ORDER BY count DESC 
            LIMIT 5
        """).fetchall()
        
        return {
            "total_products": total_products,
            "avg_price": round(avg_price, 2) if avg_price else 0,
            "total_sales": int(total_sales) if total_sales else 0,
            "avg_monthly_sales": round(avg_monthly_sales, 2) if avg_monthly_sales else 0,
            "top_categories": top_categories,
            "top_countries": top_countries
        }
    except Exception as e:
        logger.error(f"Error getting product summary: {e}")
        return {
            "total_products": 0,
            "avg_price": 0,
            "total_sales": 0,
            "avg_monthly_sales": 0,
            "top_categories": [],
            "top_countries": []
        }

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

    logger.info("Sending request to OpenAI API")
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        response.raise_for_status()
        return response
    except Exception as e:
        logger.error(f"Request error: {e}")
        raise Exception(f"Failed to get ChatCompletion response: {e}")

def ask_database(conn, query):
    """Execute an SQL query on a SQLite database."""
    try:
        logger.info(f"Executing SQL query: {query}")
        results = conn.execute(query).fetchall()
        return results
    except Exception as e:
        logger.error(f"SQL error: {e}")
        raise Exception(f"SQL error: {e}")

def plot_price_trend(product_code, conn):
    """Plot the price trend for a product."""
    query = f"""
    SELECT month, price
    FROM products
    WHERE product_code = '{product_code}'
    ORDER BY month;
    """
    logger.info(f"Plotting price trend for product: {product_code}")
    data = pd.read_sql(query, conn)
    
    if data.empty:
        st.info("No data available for plotting.")
        return None

    data['month'] = pd.to_datetime(data['month'], format='%m-%Y', errors='coerce')
    if data['month'].isnull().any():
        st.error("Date parsing error. Check the 'month' field format.")
        return None

    # Configure plot
    plt.figure(figsize=(10, 6))
    plt.style.use('seaborn-whitegrid')
    
    # Apple-inspired elegant colors
    line_color = "#0066CC"
    marker_color = "#147EFB"
    text_color = "#1D1D1F"
    grid_color = "#E5E5E5"
    
    # Create the plot
    ax = plt.gca()
    ax.plot(data['month'], data['price'], marker='o', linestyle='-', linewidth=2, 
            color=line_color, markerfacecolor=marker_color, markersize=8)
    
    # Customize appearance
    plt.title(f"Price Trend for Product {product_code}", 
              fontsize=16, fontweight='bold', color=text_color, fontname='Arial')
    plt.xlabel('Month', fontsize=12, color=text_color, fontname='Arial')
    plt.ylabel('Price ($)', fontsize=12, color=text_color, fontname='Arial')
    
    # Customize grid
    plt.grid(True, linestyle='--', alpha=0.7, color=grid_color)
    
    # Customize ticks
    plt.xticks(fontsize=10, color=text_color, fontname='Arial')
    plt.yticks(fontsize=10, color=text_color, fontname='Arial')
    
    # Add data labels
    for x, y in zip(data['month'], data['price']):
        plt.text(x, y + 2, f"${y:.2f}", 
                 ha='center', va='bottom', 
                 fontsize=9, color=text_color, 
                 fontweight='bold', fontname='Arial')
    
    # Set background color
    ax.set_facecolor('#F5F5F7')
    
    # Add annotations
    min_price = data['price'].min()
    max_price = data['price'].max()
    min_idx = data['price'].idxmin()
    max_idx = data['price'].idxmax()
    
    plt.annotate(f'Min: ${min_price:.2f}', 
                 xy=(data['month'][min_idx], min_price),
                 xytext=(data['month'][min_idx], min_price - 10),
                 arrowprops=dict(facecolor=line_color, shrink=0.05, width=1.5, headwidth=8),
                 fontsize=10, color=text_color, ha='center', fontname='Arial')
    
    plt.annotate(f'Max: ${max_price:.2f}', 
                 xy=(data['month'][max_idx], max_price),
                 xytext=(data['month'][max_idx], max_price + 10),
                 arrowprops=dict(facecolor=line_color, shrink=0.05, width=1.5, headwidth=8),
                 fontsize=10, color=text_color, ha='center', fontname='Arial')
    
    st.pyplot(plt)
    logger.info(f"Price trend plot for {product_code} created successfully")

def chat_completion_with_function_execution(messages, functions=None):
    """
    Call the ChatCompletion API and execute the function if needed.
    Returns the final text response.
    """
    try:
        logger.info("Calling chat completion with function execution")
        response = chat_completion_request(messages, functions)
        response_json = response.json()
        full_choice = response_json["choices"][0]
        full_message = full_choice["message"]
        # If API requested a function call
        if full_choice.get("finish_reason") == "function_call":
            st.write("Function call requested, executing...")
            logger.info("Function call requested, executing...")
            return call_function(messages, full_choice)
        else:
            logger.info("Received standard response from assistant")
            return full_message.get("content", "").strip()
    except Exception as e:
        logger.error(f"Error in chat completion: {e}")
        send_error_notification(
            USER_EMAIL,
            ADMIN_EMAIL,
            f"An error occurred while processing the query: {str(e)}"
        )
        st.error(f"Error occurred: {e}")
        return f"Error: {e}"

def call_function(messages, full_choice):
    """Execute the function call if required and return the final text response."""
    function_call = full_choice["message"].get("function_call", {})
    if function_call.get("name") == "ask_database":
        try:
            # Convert arguments into a dictionary
            arguments = eval(function_call.get("arguments", "{}"))
            query = arguments.get("query")
            st.write(f"Executing SQL query: {query}")
            logger.info(f"Executing SQL query from function call: {query}")
            conn = sqlite3.connect(DATABASE)
            results = ask_database(conn, query)
            conn.close()
            logger.info(f"Query executed successfully with {len(results)} results")
        except Exception as e:
            logger.error(f"SQL execution error: {e}")
            st.error(f"SQL execution error: {e}")
            send_error_notification(
                USER_EMAIL,
                ADMIN_EMAIL,
                f"Query failed: {e}"
            )
            return f"Error executing query: {e}"
        messages.append({
            "role": "function", 
            "name": "ask_database", 
            "content": str(results)
        })
        try:
            logger.info("Sending follow-up request with function results")
            followup_response = chat_completion_request(messages)
            followup_json = followup_response.json()
            return followup_json["choices"][0]["message"].get("content", "").strip()
        except Exception as e:
            logger.error(f"Follow-up function call error: {e}")
            st.error(f"Follow-up function call error: {e}")
            send_error_notification(
                USER_EMAIL,
                ADMIN_EMAIL,
                f"Follow-up function call failed: {e}"
            )
            return f"Error in follow-up function call: {e}"
    else:
        logger.error(f"Function not recognized: {function_call.get('name')}")
        st.error("Function not recognized")
        return "Error: Function not recognized"

# System message for the database assistant
agent_system_message = """You are DatabaseGPT, a helpful assistant who retrieves answers to user questions from the Database.
Provide as many details as possible to your users.
Begin!"""

# Example queries to suggest to the user
def get_example_queries():
    return [
        "What are the top 5 best-selling products?",
        "Show me products with prices above $500",
        "Which products have the highest profit margin?",
        "How many products do we have in each category?",
        "Compare sales between different product categories",
        "What's the price trend for product_code A1234?",
        "Which country of origin has the most products?",
        "Find products with low stock levels (less than 10 units)",
        "What's the average price by product category?",
        "Show monthly sales data for the last quarter"
    ]

# Add custom CSS with Apple-inspired design
def load_css():
    # Apple-inspired elegant dark typography on light background
    css = '''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #333333;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #212121;
        font-weight: 600;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #F5F7FA !important;
        border-right: none;
        padding: 0 !important;
    }
    
    .stSidebar {
        background-color: #F5F7FA !important;
    }

    .stSidebar > div {
        background-color: #F5F7FA !important;
    }

    /* Custom sidebar header */
    .sidebar-header {
        padding: 20px 0;
        text-align: center;
        border-bottom: 1px solid #e0e0e0;
        background-color: #F5F7FA !important;
    }
    
    .sidebar-section {
        padding: 20px;
        border-bottom: 1px solid #e0e0e0;
        background-color: #F5F7FA !important;
    }
    
    .sidebar-title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 15px;
        color: #212121;
    }
    
    .sidebar-metric {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        font-size: 13px;
        color: #333333;
    }
    
    .sidebar-metric-value {
        font-weight: 600;
        color: #0066cc;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: white;
        color: #333333;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 12px;
        font-size: 15px;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0066cc;
        box-shadow: 0 0 0 4px rgba(0,102,204,0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #0055b3;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Message styling */
    .user-message {
        background-color: #E6F1FF;
        border-radius: 12px;
        padding: 15px;
        margin: 12px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        position: relative;
        border-left: 3px solid #0066cc;
        border: 1px solid #e0e0e0;
    }
    
    .assistant-message {
        background-color: #FFF0F5;
        border-radius: 12px;
        padding: 15px;
        margin: 12px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        position: relative;
        border-left: 3px solid #FF69B4;
        border: 1px solid #e0e0e0;
    }
    
    .function-message {
        background-color: #f5f5f5;
        border-radius: 12px;
        padding: 15px;
        margin: 12px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-family: 'SF Mono', 'Menlo', monospace;
        font-size: 13px;
        border-left: 3px solid #666666;
        border: 1px solid #e0e0e0;
    }
    
    .message-header {
        font-weight: 600;
        margin-bottom: 8px;
        font-size: 14px;
        color: #212121;
    }
    
    /* Card styling */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.2s;
        border: 1px solid #e0e0e0;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Logo styling */
    .logo-text {
        font-family: 'Inter', sans-serif;
        font-size: 24px;
        font-weight: 600;
        color: #212121;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 15px 0;
        font-size: 12px;
        color: #666666;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Hint containers */
    .hint-container {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px 12px;
        margin: 8px 0;
        border-left: 2px solid #0066cc;
        font-size: 13px;
        border: 1px solid #e0e0e0;
    }
    
    .hint-header {
        font-weight: 600;
        color: #0066cc;
        margin-bottom: 4px;
        font-size: 13px;
    }
    
    /* Toggle sidebar button */
    .sidebar-toggle {
        position: fixed;
        top: 55px;
        left: 0;
        z-index: 99;
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #e0e0e0;
        border-left: none;
        border-radius: 0 4px 4px 0;
        width: 24px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05);
        font-size: 12px;
        transition: all 0.3s;
    }
    
    /* Log styling */
    .log-container {
        background-color: white;
        border-radius: 8px;
        padding: 12px;
        margin-top: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
    }
    
    .log-entry {
        padding: 6px 8px;
        margin: 4px 0;
        border-radius: 4px;
        font-family: 'SF Mono', 'Menlo', monospace;
        font-size: 12px;
        white-space: pre-wrap;
        word-break: break-word;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        color: #333333 !important; /* Добавлен черный цвет текста */
    }
    
    .log-info {
        border-left: 2px solid #0066cc;
    }
    
    .log-error {
        border-left: 2px solid #ff3b30;
    }
    
    .log-warning {
        border-left: 2px solid #ff9500;
    }
    
    .log-debug {
        border-left: 2px solid #34c759;
    }
    
    /* Query examples in sidebar */
    .query-example {
        background-color: #ffffff;
        padding: 8px 12px;
        border-radius: 6px;
        margin-bottom: 8px;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s;
        border-left: 2px solid transparent;
        border: 1px solid #e0e0e0;
    }
    
    .query-example:hover {
        border-left-color: #0066cc;
        background-color: #f8f9fa;
    }
    
    /* Category chips */
    .category-chip {
        display: inline-block;
        padding: 4px 10px;
        background-color: #ffffff;
        border-radius: 20px;
        font-size: 12px;
        margin-right: 6px;
        margin-bottom: 6px;
        color: #333333;
        border: 1px solid #e0e0e0;
    }
    
    /* Header section */
    .header-section {
        padding: 20px 0;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .sidebar .sidebar-content {
            width: 100%;
        }
    }
    
    /* Make expander headers more elegant */
    .streamlit-expanderHeader {
        font-size: 14px;
        font-weight: 500;
        color: #212121;
    }
    
    .streamlit-expanderHeader:hover {
        color: #0066cc;
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Display logs in an elegant container
def display_logs(num_logs=10):
    """Display the last few log entries in an elegant format"""
    try:
        with open("app.log", "r", encoding='utf-8') as log_file:
            # Read the last num_logs lines
            logs = log_file.readlines()[-num_logs:]
            
        st.markdown("""
        <div class="card">
            <h3 style="font-size: 18px; margin-bottom: 12px; color: #333333;">System Activity Logs</h3>
            <div class="log-container">
        """, unsafe_allow_html=True)
        
        for log in logs:
            log_class = "log-info"
            if "ERROR" in log:
                log_class = "log-error"
            elif "WARNING" in log:
                log_class = "log-warning"
            elif "DEBUG" in log:
                log_class = "log-debug"
                
            st.markdown(f'''
            <div class="log-entry {log_class}" style="color: #333333 !important;">
                {log}
            </div>
            ''', unsafe_allow_html=True)
            
        st.markdown("</div></div>", unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error displaying logs: {e}")
        st.error(f"Could not display logs: {e}")

# Main application logic
def main():
    # Load custom CSS
    load_css()
    
    # Initialize conversation
    conversation = Conversation()
    conn = sqlite3.connect(DATABASE)
    logger.info("Database connection established")
    
    # Get product summary stats
    product_summary = get_product_summary(conn)
    
    # Database schema description
    database_schema_string = """
    Table: products
    Columns: id, product_code, product_name, category, color, capacity, price, monthly_sales, stock_remaining, segment, discount, country_of_origin, product_index, flag, month
    """
    
    # Initialize conversation with system message
    conversation.add_message("system", agent_system_message)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    if "query_input" not in st.session_state:
        st.session_state.query_input = ""
    
    if "show_sidebar" not in st.session_state:
        st.session_state.show_sidebar = True
    
    # Define OpenAI functions
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
    
    # Sidebar setup
    with st.sidebar:
        st.markdown('<div class="sidebar-header" style="background-color: #F5F7FA; color: #333333;">', unsafe_allow_html=True)
        st.markdown('''
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column; padding: 10px 0; background-color: #F5F7FA; color: #333333;">
            <svg viewBox="0 0 17 48" width="17" height="30" style="margin-bottom: 8px;">
                <path d="m15.5752 19.0792a4.2055 4.2055 0 0 0 -2.01 3.5376 4.0931 4.0931 0 0 0 2.4908 3.7542 9.7779 9.7779 0 0 1 -1.2755 2.6351c-.7941 1.1431-1.6244 2.2862-2.8878 2.2862s-1.5883-.734-3.0171-.734c-1.3896 0-1.8993.7581-3.0171.7581s-1.9239-1.0669-2.8324-2.3495a11.3987 11.3987 0 0 1 -1.9-6.1487c0-3.619 2.3471-5.5451 4.6655-5.5451 1.2248 0 2.2487.8182 3.0171.8182.734 0 1.8832-.8789 3.29-.8789a4.7267 4.7267 0 0 1 3.9628 2.0073zm-7.3628-2.2207a4.5037 4.5037 0 0 0 1.0669-3.290 3.9884 3.9884 0 0 0 -2.5868 1.3377 4.1164 4.1164 0 0 0 -1.109 3.17 3.6039 3.6039 0 0 0 2.6289-1.2177z" fill="#000000"></path>
            </svg>
            <div style="font-weight:600; font-size:16px; color: #333333;">Product Analytics</div>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add product statistics
        st.markdown('<div class="sidebar-section" style="background-color: #F5F7FA; color: #333333; border-bottom: 1px solid #e0e0e0;">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title" style="font-size: 16px; font-weight: 600; margin-bottom: 15px; color: #333333;">Product Dashboard</div>', unsafe_allow_html=True)
        
        # Show product stats in elegant format
        st.markdown(f'''
        <div class="sidebar-metric" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 13px; color: #333333;">
            <span>Total Products:</span>
            <span class="sidebar-metric-value" style="font-weight: 600; color: #0066cc;">{product_summary["total_products"]}</span>
        </div>
        <div class="sidebar-metric" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 13px; color: #333333;">
            <span>Average Price:</span>
            <span class="sidebar-metric-value" style="font-weight: 600; color: #0066cc;">${product_summary["avg_price"]}</span>
        </div>
        <div class="sidebar-metric" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 13px; color: #333333;">
            <span>Average Price:</span>
            <span class="sidebar-metric-value" style="font-weight: 600; color: #0066cc;">${product_summary["avg_price"]}</span>
        </div>
        <div class="sidebar-metric" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 13px; color: #333333;">
            <span>Total Monthly Sales:</span>
            <span class="sidebar-metric-value" style="font-weight: 600; color: #0066cc;">{product_summary["total_sales"]}</span>
        </div>
        <div class="sidebar-metric" style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 13px; color: #333333;">
            <span>Avg Sales Per Product:</span>
            <span class="sidebar-metric-value" style="font-weight: 600; color: #0066cc;">{product_summary["avg_monthly_sales"]}</span>
        </div>
        ''', unsafe_allow_html=True)
        
        # Top categories visualization
        if product_summary["top_categories"]:
            st.markdown('<div style="margin-top:15px; background-color: #F5F7FA; color: #333333;">', unsafe_allow_html=True)
            st.markdown('<div style="font-weight:500; margin-bottom:8px; font-size:14px; color: #333333;">Top Categories</div>', unsafe_allow_html=True)
            
            for category, count in product_summary["top_categories"]:
                if category:  # Avoid None categories
                    percentage = (count / product_summary["total_products"]) * 100
                    st.markdown(f'''
                    <div style="margin-bottom:8px; background-color: #F5F7FA;">
                        <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px; color: #333333;">
                            <span>{category}</span>
                            <span>{count} products</span>
                        </div>
                        <div style="height:6px; background-color:#f0f0f0; border-radius:3px; overflow:hidden;">
                            <div style="height:100%; width:{percentage}%; background-color:#0066cc; border-radius:3px;"></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add query suggestions section
        st.markdown('<div class="sidebar-section" style="background-color: #F5F7FA; color: #333333; border-bottom: 1px solid #e0e0e0;">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title" style="font-size: 16px; font-weight: 600; margin-bottom: 15px; color: #333333;">Example Queries</div>', unsafe_allow_html=True)
        
        example_queries = get_example_queries()
        for i, query in enumerate(example_queries[:5]):
            query_id = f"query_{i}"
            if st.button(query, key=query_id):
                st.session_state.query_input = query
        
        with st.expander("More Examples"):
            for i, query in enumerate(example_queries[5:]):
                query_id = f"query_more_{i}"
                if st.button(query, key=query_id):
                    st.session_state.query_input = query
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add query tips section
        st.markdown('<div class="sidebar-section" style="background-color: #F5F7FA; color: #333333; border-bottom: 1px solid #e0e0e0;">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title" style="font-size: 16px; font-weight: 600; margin-bottom: 15px; color: #333333;">Query Tips</div>', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="hint-container" style="background-color: white; border-radius: 8px; padding: 10px 12px; margin: 8px 0; border-left: 2px solid #0066cc; font-size: 13px; border: 1px solid #e0e0e0; color: #333333;">
            <div class="hint-header" style="font-weight: 600; color: #333333; margin-bottom: 4px; font-size: 13px;">Product Details</div>
            <p style="color: #333333;">Try "Tell me about product_code X123" to get full details.</p>
        </div>
        <div class="hint-container" style="background-color: white; border-radius: 8px; padding: 10px 12px; margin: 8px 0; border-left: 2px solid #0066cc; font-size: 13px; border: 1px solid #e0e0e0; color: #333333;">
            <div class="hint-header" style="font-weight: 600; color: #333333; margin-bottom: 4px; font-size: 13px;">Price Comparisons</div>
            <p style="color: #333333;">Ask "Compare prices in categories A and B" for insights.</p>
        </div>
        <div class="hint-container" style="background-color: white; border-radius: 8px; padding: 10px 12px; margin: 8px 0; border-left: 2px solid #0066cc; font-size: 13px; border: 1px solid #e0e0e0; color: #333333;">
            <div class="hint-header" style="font-weight: 600; color: #333333; margin-bottom: 4px; font-size: 13px;">Sales Analysis</div>
            <p style="color: #333333;">Try "Show me monthly sales trends" for visualizations.</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    # Header section
    st.markdown('''
    <div class="header-section" style="padding: 20px 0; text-align: center; margin-bottom: 20px; background-color: white;">
        <h1 class="logo-text" style="font-family: 'Inter', sans-serif; font-size: 24px; font-weight: 600; color: black; text-align: center; letter-spacing: -0.5px;">Database Query Assistant</h1>
    </div>
    ''', unsafe_allow_html=True)
    
    # If sidebar is hidden, show toggle button
    if not st.session_state.show_sidebar:
        if st.button("» Show Analytics Panel"):
            st.session_state.show_sidebar = True
            st.rerun()
    
    # Welcome card
    # Add custom CSS for card and category-chip
    st.markdown('''
    <style>
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        color: black;
    }
    .category-chip {
        display: inline-block;
        padding: 4px 10px;
        background-color: white;
        border-radius: 20px;
        font-size: 12px;
        margin-right: 6px;
        margin-bottom: 6px;
        color: black;
        border: 1px solid #e0e0e0;
    }
    </style>
    ''', unsafe_allow_html=True)

    # Welcome card
    st.markdown('''
    <div class="card" style="background-color: white; color: black;">
        <h3 style="font-size: 20px; margin-bottom: 15px; color: black;">👋 Welcome to the Database Query Assistant</h3>
        <p style="margin-bottom: 15px; color: black;">Ask questions about our product database and get instant insights. Our AI assistant will answer your questions based on product data.</p>
    
        
        
    </div>
    ''', unsafe_allow_html=True)
    
    # Display conversation messages with improved styling
    for message in st.session_state["messages"]:
        role = message['role']
        content = message['content']
        
        if role == "user":
            st.markdown(f'''
            <div class="user-message" style="background-color: #E6F1FF; border-radius: 12px; padding: 15px; margin: 12px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); position: relative; border-left: 3px solid #0066cc; border: 1px solid #e0e0e0; color: #333333;">
                <div class="message-header" style="font-weight: 600; margin-bottom: 8px; font-size: 14px; color: #212121;">You</div>
                <div style="color: #333333;">{content}</div>
            </div>
            ''', unsafe_allow_html=True)
        elif role == "assistant":
            st.markdown(f'''
            <div class="assistant-message" style="background-color: #FFF0F5; border-radius: 12px; padding: 15px; margin: 12px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); position: relative; border-left: 3px solid #FF69B4; border: 1px solid #e0e0e0; color: #333333;">
                <div class="message-header" style="font-weight: 600; margin-bottom: 8px; font-size: 14px; color: #212121;">Assistant</div>
                <div style="color: #333333;">{content}</div>
            </div>
            ''', unsafe_allow_html=True)
        elif role == "function":
            st.markdown(f'''
            <div class="function-message" style="background-color: #F5F5F5; border-radius: 12px; padding: 15px; margin: 12px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); font-family: 'SF Mono', 'Menlo', monospace; font-size: 13px; border-left: 3px solid #666666; border: 1px solid #e0e0e0; color: #333333;">
                <div class="message-header" style="font-weight: 600; margin-bottom: 8px; font-size: 14px; color: #212121;">System</div>
                <pre style="color: #333333;">{content}</pre>
            </div>
            ''', unsafe_allow_html=True)
    
    # Query input
    st.markdown('<div class="card" style="background-color: white; color: black;">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        query_input = st.text_input(
            "Ask about products...",
            key="query_input",
            label_visibility="collapsed",
            placeholder="Ask a question about products, sales, or inventory..."
        )
    
    with col2:
        submit_button = st.button("Ask", key="query_submit_btn")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process query when submitted
    if submit_button and query_input:
        if query_input not in [msg['content'] for msg in st.session_state["messages"] if msg['role'] == 'user']:
            logger.info(f"New query received: {query_input}")
            
            # Add to conversation
            conversation.add_message("user", query_input)
            st.session_state["messages"].append({"role": "user", "content": query_input})
            
            # Send email notification for new query
            send_email_notification(
                user_email=USER_EMAIL,
                admin_email=ADMIN_EMAIL,
                subject="🔍 New Query Received",
                body=f"User with email {USER_EMAIL} has asked a query: '{query_input}'"
            )
            
            # Get response from the assistant
            logger.info("Getting response from assistant")
            assistant_response = chat_completion_with_function_execution(conversation.messages, functions=functions)
            conversation.add_message("assistant", assistant_response)
            st.session_state["messages"].append({"role": "assistant", "content": assistant_response})
            logger.info("Response added to conversation")
            
            # Отправляем уведомление с ответом ассистента
            try:
                logger.info(f"Sending assistant response email notification")
                send_assistant_response_notification(
                    user_email=USER_EMAIL,
                    admin_email=ADMIN_EMAIL,
                    query_text=query_input,
                    assistant_response=assistant_response
                )
                logger.info("Email with assistant response sent successfully")
            except Exception as e:
                logger.error(f"Error sending assistant response email: {e}")
            
            # If query contains "product_code", plot the price trend
            if "product_code" in query_input.lower():
                try:
                    # Extract product code - simple approach, could be enhanced
                    words = query_input.split()
                    for i, word in enumerate(words):
                        if word.lower() == "product_code" and i < len(words) - 1:
                            product_code = words[i+1].strip(",.?!:;'\"")
                            plot_price_trend(product_code, conn)
                            logger.info(f"Price trend plotted for product code: {product_code}")
                            break
                except Exception as e:
                    logger.error(f"Error plotting price trend: {e}")
                    st.error(f"Could not generate price trend: {e}")
            
            # Rerun to update UI
            st.rerun()
        else:
            logger.warning("Duplicate query detected")
            st.warning("You've already asked this query.")
    
    # Display system logs in expandable section
    with st.expander("System Logs"):
        display_logs(20)
    
    # Footer
    st.markdown('''
    <div class="footer" style="text-align: center; margin-top: 40px; padding: 15px 0; font-size: 12px; color: black; border-top: 1px solid #e0e0e0; background-color: white;">
        <p style="color: black;">© 2025 Database Query Assistant | Developed as a Capstone Project</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Close database connection
    conn.close()

if __name__ == '__main__':
    main()
