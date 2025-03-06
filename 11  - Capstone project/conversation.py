from termcolor import colored
import datetime
import json
import os

class Conversation:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        """Добавить сообщение в разговор"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.now().isoformat()
        })

    def display_conversation(self, detailed=False):
        """Отобразить разговор в терминале с цветами"""
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta",
        }

        for message in self.messages:
            timestamp = f"[{message['timestamp']}] " if detailed else ""
            formatted_message = f"{timestamp}{message['role']}: {message['content']}\n"
            print(colored(formatted_message, role_to_color.get(message["role"], "white")))

    def save_conversation(self, filename="conversation.json", folder="."):
        """Сохранить историю разговора в файл JSON"""
        filepath = os.path.join(folder, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(self.messages, file, indent=4, ensure_ascii=False)
            print(colored(f"Conversation saved to {filepath}", "green"))
        except (OSError, IOError) as e:
            print(colored(f"Ошибка сохранения: {e}", "red"))
