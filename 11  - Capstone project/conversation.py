from termcolor import colored
import datetime
import json
import os
from logger import logger, log_debug, log_error, log_info

class Conversation:
    def __init__(self):
        self.messages = []
        log_debug("Initialized new conversation")

    def add_message(self, role, content):
        """Добавить сообщение в разговор"""
        timestamp = datetime.datetime.now().isoformat()
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": timestamp
        })
        log_debug(f"Added {role} message: {content[:50]}...")

    def display_conversation(self, detailed=False):
        """Отобразить разговор в терминале с цветами и элегантным форматированием"""
        if not self.messages:
            print(colored("Conversation is empty.", "yellow"))
            return

        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }
        
        role_to_emoji = {
            "system": "🔧",
            "user": "👤",
            "assistant": "🤖",
            "function": "⚙️",
        }
        
        print(colored("┌" + "─" * 80 + "┐", "white"))
        print(colored("│ " + " " * 28 + "CONVERSATION HISTORY" + " " * 28 + " │", "white"))
        print(colored("├" + "─" * 80 + "┤", "white"))

        for i, message in enumerate(self.messages):
            # Format timestamp if detailed view requested
            timestamp = f"[{message['timestamp']}] " if detailed else ""
            
            # Get role emoji and color
            emoji = role_to_emoji.get(message["role"], "📝")
            color = role_to_color.get(message["role"], "white")
            
            # Format the message with proper wrapping
            role_display = f"{emoji} {message['role'].upper()}"
            content_lines = self._wrap_text(message['content'], 75)  # Wrap at 75 chars
            
            # Print message header
            print(colored(f"│ {timestamp}{role_display}", color) + " " * (79 - len(timestamp) - len(role_display)) + colored("│", "white"))
            print(colored("│" + "─" * 80 + "│", "white"))
            
            # Print message content with wrapping
            for line in content_lines:
                padding = " " * (80 - len(line))
                print(colored(f"│ {line}{padding}│", "white"))
            
            # Print separator between messages, except for the last one
            if i < len(self.messages) - 1:
                print(colored("├" + "─" * 80 + "┤", "white"))
            else:
                print(colored("└" + "─" * 80 + "┘", "white"))

    def _wrap_text(self, text, width):
        """Wrap text to a specified width"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= width:  # +1 for the space
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:  # Add the last line if it exists
            lines.append(" ".join(current_line))
            
        return lines

    def save_conversation(self, filename="conversation.json", folder="."):
        """Сохранить историю разговора в файл JSON с элегантным форматированием"""
        filepath = os.path.join(folder, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(self.messages, file, indent=4, ensure_ascii=False)
            
            # Get file size for logging
            file_size = os.path.getsize(filepath)
            log_info(f"Conversation saved to {filepath} ({file_size} bytes)")
            
            # Print success message with frame
            print(colored("┌" + "─" * 80 + "┐", "green"))
            print(colored("│ " + " " * 25 + "CONVERSATION SAVED" + " " * 26 + " │", "green"))
            print(colored("│ " + f"File: {filepath}" + " " * (79 - len(f"File: {filepath}")) + "│", "green"))
            print(colored("│ " + f"Size: {file_size} bytes" + " " * (79 - len(f"Size: {file_size} bytes")) + "│", "green"))
            print(colored("└" + "─" * 80 + "┘", "green"))
        except (OSError, IOError) as e:
            error_msg = f"Error saving conversation: {e}"
            log_error(error_msg)
            print(colored("┌" + "─" * 80 + "┐", "red"))
            print(colored("│ " + " " * 25 + "SAVE ERROR" + " " * 33 + " │", "red"))
            print(colored("│ " + error_msg + " " * (79 - len(error_msg)) + "│", "red"))
            print(colored("└" + "─" * 80 + "┘", "red"))

    def load_conversation(self, filename="conversation.json", folder="."):
        """Загрузить историю разговора из файла JSON"""
        filepath = os.path.join(folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                self.messages = json.load(file)
            log_info(f"Loaded conversation from {filepath} with {len(self.messages)} messages")
            return True
        except (OSError, IOError, json.JSONDecodeError) as e:
            log_error(f"Error loading conversation: {e}")
            return False

    def get_summary(self):
        """Получить краткую сводку о разговоре"""
        if not self.messages:
            return "No messages in conversation."
        
        user_messages = sum(1 for m in self.messages if m["role"] == "user")
        assistant_messages = sum(1 for m in self.messages if m["role"] == "assistant")
        system_messages = sum(1 for m in self.messages if m["role"] == "system")
        function_messages = sum(1 for m in self.messages if m["role"] == "function")
        
        first_timestamp = datetime.datetime.fromisoformat(self.messages[0]["timestamp"])
        last_timestamp = datetime.datetime.fromisoformat(self.messages[-1]["timestamp"])
        duration = last_timestamp - first_timestamp
        
        return {
            "total_messages": len(self.messages),
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "system_messages": system_messages,
            "function_messages": function_messages,
            "start_time": first_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": last_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": str(duration),
        }
