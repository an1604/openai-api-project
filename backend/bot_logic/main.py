import sys

sys.path.append(".")
import os
from tool_chatbot.utils import LeavingChat, get_bot_configuration
from tool_chatbot.chatbot_wrapper import ChatBot
import json
import openai
from dotenv import load_dotenv

load_dotenv('.env')

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_version = os.getenv('OPENAI_API_VERSION')

if __name__ == "__main__":
    chatbot = ChatBot(**get_bot_configuration())
    try:
        response = chatbot.generate_initial_message()
        print("assistant: " + response)
        while True:
            user_input = input("User: ")
            try:
                response = chatbot.generate_response(user_input=user_input)
                print(f"Assistant: {response}")
                # # Get messages since user_input
                # messages = chatbot.chat_history.get_window()
                # index = [m["content"] for m in messages].index(user_input) + 1
                # messages = messages[index:]
                # for message in messages:
                #     print(message["role"] + ": " + message["content"])
            except LeavingChat:
                print("You have left the chat.")
                break
    except KeyboardInterrupt:
        with open("bot_logic/chat_history.json", "w") as f:
            json.dump(chatbot.chat_history.history, f, indent=4)
        print("Chat history saved to chat_history.json")
