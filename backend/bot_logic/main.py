import sys
import time

sys.path.append("..")
import os
from tool_chatbot.exceptions import LeavingChat
from tool_chatbot.utils import get_bot_configuration
from tool_chatbot.chatbot_wrapper import ChatBot
import json
import openai
from dotenv import load_dotenv
from openai.error import RateLimitError
from tool_chatbot.moderation import ModerationModel
import datetime

load_dotenv('../.env')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_version = os.getenv('OPENAI_API_VERSION')


def save_conversation_in_chat_history(chatbot: ChatBot):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bot_logic/chat_history_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(chatbot.chat_history.history, f, indent=4)

    print(f"Chat history saved to {filename}")


if __name__ == "__main__":
    chatbot = ChatBot(**get_bot_configuration())
    moderation_model = ModerationModel()
    last_input = None  # Handle the API limitation.
    try:
        response = chatbot.generate_initial_message()
        print("\nassistant: " + response)
        while True:
            if not last_input:
                user_input = input("\nUser: ")
                # input restriction and violating content checking before generating response.
                if not moderation_model.predict_violating_content(user_input):
                    try:
                        response = chatbot.generate_response(user_input=user_input)
                        print(f"\nAssistant: {response}")
                        last_input = None
                    except LeavingChat:
                        print("You have left the chat.")
                        break
                    except RateLimitError as e:
                        #print('A RateLimitError occurred, waiting 20 seconds...{}'.format(e))
                        time.sleep(20)
                        last_input = user_input
                else:
                    response = ('I cant pay attention to your previous message, Its against my rules, please try '
                                'again.')
            else:
                response = chatbot.generate_response(last_input)
                last_input = None
                print("assistant: " + response)

    except KeyboardInterrupt:
        save_conversation_in_chat_history(chatbot)
