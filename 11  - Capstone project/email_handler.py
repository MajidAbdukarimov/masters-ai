import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_elegant_email_template(email_type, content, user_email=None):
    """
    Creates an elegant HTML email template based on type.
    
    :param email_type: Type of email ('query', 'error', 'results')
    :param content: Main content to include in the email
    :param user_email: User email for personalization
    :return: HTML string
    """
    # Get current date and time
    current_time = datetime.datetime.now()
    formatted_date = current_time.strftime("%A, %B %d, %Y")
    formatted_time = current_time.strftime("%I:%M %p")
    current_year = current_time.year
    
    # Base styles for all emails
    base_styles = """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #1d1d1f;
            background-color: #f5f5f7;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .header {
            padding: 24px;
            text-align: center;
            background-color: #f5f5f7;
            border-bottom: 1px solid #d2d2d7;
        }
        .logo {
            margin-bottom: 12px;
        }
        .title {
            font-size: 24px;
            font-weight: 600;
            color: #1d1d1f;
            margin: 0;
        }
        .subtitle {
            font-size: 16px;
            color: #86868b;
            margin: 8px 0 0 0;
        }
        .content {
            padding: 32px 24px;
            background-color: #ffffff;
        }
        .section-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #1d1d1f;
        }
        .message {
            background-color: #f5f5f7;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 24px;
            border-left: 4px solid #0066cc;
        }
        .message-heading {
            font-weight: 600;
            margin-bottom: 8px;
        }
        .details {
            background-color: #f5f5f7;
            border-radius: 8px;
            padding: 16px;
            margin-top: 24px;
        }
        .detail-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 14px;
        }
        .detail-label {
            color: #86868b;
        }
        .detail-value {
            font-weight: 600;
            color: #1d1d1f;
        }
        .cta-button {
            display: inline-block;
            background-color: #0066cc;
            color: #ffffff;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            margin-top: 24px;
            margin-bottom: 8px;
        }
        .footer {
            background-color: #f5f5f7;
            padding: 24px;
            text-align: center;
            font-size: 12px;
            color: #86868b;
            border-top: 1px solid #d2d2d7;
        }
        .status-indicator {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-success {
            background-color: #34c759;
        }
        .status-error {
            background-color: #ff3b30;
        }
        .status-info {
            background-color: #0066cc;
        }
        .divider {
            height: 1px;
            background-color: #d2d2d7;
            margin: 24px 0;
        }
    """
    
    # Email header with Apple-inspired design
    email_header = f"""
    <div class="header">
        <div class="logo">
            <svg width="40" height="40" viewBox="0 0 17 48" style="fill:#1d1d1f;">
                <path d="m15.5752 19.0792a4.2055 4.2055 0 0 0 -2.01 3.5376 4.0931 4.0931 0 0 0 2.4908 3.7542 9.7779 9.7779 0 0 1 -1.2755 2.6351c-.7941 1.1431-1.6244 2.2862-2.8878 2.2862s-1.5883-.734-3.0171-.734c-1.3896 0-1.8993.7581-3.0171.7581s-1.9239-1.0669-2.8324-2.3495a11.3987 11.3987 0 0 1 -1.9-6.1487c0-3.619 2.3471-5.5451 4.6655-5.5451 1.2248 0 2.2487.8182 3.0171.8182.734 0 1.8832-.8789 3.29-.8789a4.7267 4.7267 0 0 1 3.9628 2.0073zm-7.3628-2.2207a4.5037 4.5037 0 0 0 1.0669-3.290 3.9884 3.9884 0 0 0 -2.5868 1.3377 4.1164 4.1164 0 0 0 -1.109 3.17 3.6039 3.6039 0 0 0 2.6289-1.2177z"></path>
            </svg>
        </div>
    """
    
    # Email content based on type
    if email_type == 'query':
        # New query notification
        title = "New Query Received"
        subtitle = "Database Query Assistant notification"
        status_class = "status-info"
        email_header += f"""
        <h1 class="title">{title}</h1>
        <p class="subtitle">{subtitle}</p>
    </div>
    <div class="content">
        <div class="section-title">
            <span class="status-indicator {status_class}"></span>New Query Details
        </div>
        <div class="message">
            <div class="message-heading">Query</div>
            <p>{content}</p>
        </div>
        <div class="details">
            <div class="detail-row">
                <span class="detail-label">Date</span>
                <span class="detail-value">{formatted_date}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Time</span>
                <span class="detail-value">{formatted_time}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">User</span>
                <span class="detail-value">{user_email if user_email else 'Anonymous'}</span>
            </div>
        </div>
        <center>
            <a href="#" class="cta-button">View in Dashboard</a>
        </center>
        """
    
    elif email_type == 'error':
        # Error notification
        title = "Error Detected"
        subtitle = "An issue requires your attention"
        status_class = "status-error"
        email_header += f"""
        <h1 class="title">{title}</h1>
        <p class="subtitle">{subtitle}</p>
    </div>
    <div class="content">
        <div class="section-title">
            <span class="status-indicator {status_class}"></span>Error Details
        </div>
        <div class="message">
            <div class="message-heading">Error Message</div>
            <p>{content}</p>
        </div>
        <div class="details">
            <div class="detail-row">
                <span class="detail-label">Date</span>
                <span class="detail-value">{formatted_date}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Time</span>
                <span class="detail-value">{formatted_time}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">User</span>
                <span class="detail-value">{user_email if user_email else 'Anonymous'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Status</span>
                <span class="detail-value" style="color:#ff3b30;">Requires Attention</span>
            </div>
        </div>
        <center>
            <a href="#" class="cta-button">View System Logs</a>
        </center>
        """
    
    elif email_type == 'results':
        # Results notification
        title = "Query Results Ready"
        subtitle = "Your database query has been processed"
        status_class = "status-success"
        
        # Handle both string and dictionary content
        if isinstance(content, dict):
            query = content.get('query', 'N/A')
            record_count = content.get('record_count', 'N/A')
            processing_time = content.get('processing_time', 'N/A')
        else:
            query = content
            record_count = 'N/A'
            processing_time = 'N/A'
            
        email_header += f"""
        <h1 class="title">{title}</h1>
        <p class="subtitle">{subtitle}</p>
    </div>
    <div class="content">
        <div class="section-title">
            <span class="status-indicator {status_class}"></span>Results Summary
        </div>
        <div class="message">
            <div class="message-heading">Original Query</div>
            <p>{query}</p>
        </div>
        
        <div class="section-title">Results Overview</div>
        <div class="details">
            <div class="detail-row">
                <span class="detail-label">Records Found</span>
                <span class="detail-value">{record_count}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Processing Time</span>
                <span class="detail-value">{processing_time} ms</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Date Generated</span>
                <span class="detail-value">{formatted_date}</span>
            </div>
        </div>
        
        <div class="divider"></div>
        
        <center>
            <a href="#" class="cta-button">View Full Results</a>
        </center>
        """
    
    # Common footer for all email types
    footer = f"""
        <div class="footer">
            <p>This is an automated message from the Database Query Assistant.</p>
            <p>© {current_year} Database Query Assistant. All rights reserved.</p>
        </div>
    """
    
    # Assemble the complete HTML email
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title if 'title' in locals() else 'Database Query Assistant'}</title>
        <style>
            {base_styles}
        </style>
    </head>
    <body>
        <div class="container">
            {email_header}
            {footer}
        </div>
    </body>
    </html>
    """
    
    return html

def send_email_notification(user_email, admin_email, subject, body=None, html_body=None):
    """
    Sends an email notification to the admin with the specified subject and body.
    
    :param user_email: The sender's email (user email).
    :param admin_email: The recipient's email (admin email).
    :param subject: Subject of the email.
    :param body: Plain text body of the email (optional if html_body is provided).
    :param html_body: HTML formatted body of the email (optional).
    """
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        logging.error("Email credentials are missing")
        return

    # Create a multipart message
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = admin_email
    message["Subject"] = subject
    
    # Current timestamp for the email
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add plain text version if provided
    if body:
        # Add timestamp to plain text body
        enhanced_body = f"[{current_time}]\n\n{body}\n\nSent from Database Query Assistant"
        message.attach(MIMEText(enhanced_body, "plain"))
    
    # If HTML body is provided, use it
    if html_body:
        message.attach(MIMEText(html_body, "html"))
    # Otherwise, create an HTML version based on the plain text body
    elif body:
        # Generate elegant HTML email based on subject
        if "Error" in subject:
            html = create_elegant_email_template('error', body, user_email)
        elif "Query" in subject:
            html = create_elegant_email_template('query', body, user_email)
        else:
            # Default email template with the provided body
            html = create_elegant_email_template('results', body, user_email)
        
        message.attach(MIMEText(html, "html"))

    try:
        logging.info(f"Sending email with subject: {subject}")
        with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, admin_email, message.as_string())
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

def send_query_notification(user_email, admin_email, query_text):
    """
    Send an elegant notification about a new query.
    
    :param user_email: The user's email address
    :param admin_email: The admin's email address to notify
    :param query_text: The text of the query
    """
    subject = "🔍 New Query Received"
    
    # Create elegant HTML email for the query notification
    html_body = create_elegant_email_template('query', query_text, user_email)
    
    # Send the notification
    send_email_notification(user_email, admin_email, subject, body=query_text, html_body=html_body)

def send_error_notification(user_email, admin_email, error_message):
    """
    Send an elegant notification about an error.
    
    :param user_email: The user's email address
    :param admin_email: The admin's email address to notify
    :param error_message: The error message to include
    """
    subject = "⚠️ Error in Database Query Assistant"
    
    # Create elegant HTML email for the error notification
    html_body = create_elegant_email_template('error', error_message, user_email)
    
    # Send the notification
    send_email_notification(user_email, admin_email, subject, body=error_message, html_body=html_body)

def send_results_notification(user_email, admin_email, query, results_info):
    """
    Send an elegant notification with query results.
    
    :param user_email: The user's email address
    :param admin_email: The admin's email address to notify
    :param query: The original query text
    :param results_info: Dictionary with results information
    """
    subject = "✅ Query Results Ready"
    
    # Prepare content for both plain text and HTML
    content = {
        'query': query,
        'record_count': results_info.get('count', 'N/A'),
        'processing_time': results_info.get('time', 'N/A')
    }
    
    # Plain text version
    plain_body = f"Your query: {query}\n\nRecords found: {content['record_count']}\nProcessing time: {content['processing_time']} ms"
    
    # Create elegant HTML email
    html_body = create_elegant_email_template('results', content, user_email)
    
    # Send the notification
    send_email_notification(user_email, admin_email, subject, body=plain_body, html_body=html_body)

def send_assistant_response_notification(user_email, admin_email, query_text, assistant_response):
    """
    Отправляет уведомление с запросом пользователя и ответом ассистента
    
    :param user_email: Email пользователя
    :param admin_email: Email администратора
    :param query_text: Текст запроса пользователя
    :param assistant_response: Ответ ассистента на запрос
    """
    subject = "🤖 Assistant Response"
    
    # Преобразуем возможные HTML-теги в безопасные для отображения строки
    safe_query = query_text.replace("<", "&lt;").replace(">", "&gt;")
    safe_response = assistant_response.replace("<", "&lt;").replace(">", "&gt;")
    
    # Добавляем переносы строк для лучшего форматирования
    safe_response = safe_response.replace("\n", "<br>")
    
    # Текущее время и дата
    current_time = datetime.datetime.now()
    formatted_date = current_time.strftime("%A, %B %d, %Y")
    formatted_time = current_time.strftime("%I:%M %p")
    current_year = current_time.year
    
    # Простой текстовый вариант
    plain_body = f"""
User Query:
{query_text}

Assistant Response:
{assistant_response}

Date: {formatted_date}
Time: {formatted_time}
User: {user_email if user_email else 'Anonymous'}

Sent from Database Query Assistant
"""
    
    # HTML версия письма
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assistant Response</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #1d1d1f;
            background-color: #f5f5f7;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            padding: 24px;
            text-align: center;
            background-color: #f5f5f7;
            border-bottom: 1px solid #d2d2d7;
        }}
        .logo {{
            margin-bottom: 12px;
        }}
        .title {{
            font-size: 24px;
            font-weight: 600;
            color: #1d1d1f;
            margin: 0;
        }}
        .subtitle {{
            font-size: 16px;
            color: #86868b;
            margin: 8px 0 0 0;
        }}
        .content {{
            padding: 32px 24px;
            background-color: #ffffff;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #1d1d1f;
        }}
        .message {{
            background-color: #f5f5f7;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 24px;
        }}
        .user-message {{
            border-left: 4px solid #0066cc;
            background-color: #E6F1FF;
        }}
        .assistant-message {{
            border-left: 4px solid #FF69B4;
            background-color: #FFF0F5;
        }}
        .message-heading {{
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .message-content {{
            margin: 0;
            color: #333333;
        }}
        .details {{
            background-color: #f5f5f7;
            border-radius: 8px;
            padding: 16px;
            margin-top: 24px;
        }}
        .detail-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 14px;
        }}
        .detail-label {{
            color: #86868b;
        }}
        .detail-value {{
            font-weight: 500;
            color: #1d1d1f;
        }}
        .cta-button {{
            display: inline-block;
            background-color: #0066cc;
            color: #ffffff !important;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            margin-top: 24px;
            margin-bottom: 8px;
        }}
        .footer {{
            background-color: #f5f5f7;
            padding: 24px;
            text-align: center;
            font-size: 12px;
            color: #86868b;
            border-top: 1px solid #d2d2d7;
        }}
        .status-indicator {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        .status-info {{
            background-color: #0066cc;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <svg width="40" height="40" viewBox="0 0 17 48" style="fill:#1d1d1f;">
                    <path d="m15.5752 19.0792a4.2055 4.2055 0 0 0 -2.01 3.5376 4.0931 4.0931 0 0 0 2.4908 3.7542 9.7779 9.7779 0 0 1 -1.2755 2.6351c-.7941 1.1431-1.6244 2.2862-2.8878 2.2862s-1.5883-.734-3.0171-.734c-1.3896 0-1.8993.7581-3.0171.7581s-1.9239-1.0669-2.8324-2.3495a11.3987 11.3987 0 0 1 -1.9-6.1487c0-3.619 2.3471-5.5451 4.6655-5.5451 1.2248 0 2.2487.8182 3.0171.8182.734 0 1.8832-.8789 3.29-.8789a4.7267 4.7267 0 0 1 3.9628 2.0073zm-7.3628-2.2207a4.5037 4.5037 0 0 0 1.0669-3.290 3.9884 3.9884 0 0 0 -2.5868 1.3377 4.1164 4.1164 0 0 0 -1.109 3.17 3.6039 3.6039 0 0 0 2.6289-1.2177z"></path>
                </svg>
            </div>
            <h1 class="title">Assistant Response</h1>
            <p class="subtitle">Database Query Assistant results</p>
        </div>
        <div class="content">
            <div class="section-title">
                <span class="status-indicator status-info"></span>Query and Response
            </div>
            
            <div class="message user-message">
                <div class="message-heading">User Query</div>
                <p class="message-content">{safe_query}</p>
            </div>
            
            <div class="message assistant-message">
                <div class="message-heading">Assistant Response</div>
                <p class="message-content">{safe_response}</p>
            </div>
            
            <div class="details">
                <div class="detail-row">
                    <span class="detail-label">Date</span>
                    <span class="detail-value">{formatted_date}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Time</span>
                    <span class="detail-value">{formatted_time}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">User</span>
                    <span class="detail-value">{user_email if user_email else 'Anonymous'}</span>
                </div>
            </div>
            
            <center>
                <a href="#" class="cta-button">View All History</a>
            </center>
        </div>
        
        <div class="footer">
            <p>This is an automated message from the Database Query Assistant.</p>
            <p>© {current_year} Database Query Assistant. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Отправляем уведомление
    send_email_notification(user_email, admin_email, subject, body=plain_body, html_body=html_body)
