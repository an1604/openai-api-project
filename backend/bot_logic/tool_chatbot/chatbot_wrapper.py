import openai
import os
import dotenv
from bot_logic.tool_chatbot.utils import ClientInfo, LeavingChat, get_log_name
from bot_logic.tool_chatbot.chat_utils import ChatMemory, get_chat_answer
from bot_logic.tool_chatbot.functions import functions
import logging
import time


dotenv.load_dotenv()


def client_info2string(client_info):
    return (f"\tAmount: {client_info.amount}\n"
            f"\tDuration: {client_info.duration}\n"
            f"\tWithdrawal Preference: {client_info.withdrawal_preference}"
            )


class ChatBot:
    def __init__(
        self,
        currency: str,
        language: str,
        product_type: str,
        first_message: str,
        prompt="bot_logic/prompts/v4_1ofer.txt",
    ):
        assert os.getenv(
            "OPENAI_API_KEY"
        ), "Please set your OPENAI_API_KEY environment variable."
        openai.api_key = os.getenv("OPENAI_API_KEY")
        # Setup storage for Client Info
        self.client_info = ClientInfo(
            amount=None,
            duration=None,
            withdrawal_preference=None,
        )
        self.chat_history = ChatMemory(token_limit=3896, functions=functions)
        with open(prompt, "r") as f:
            self.prompt = f.read()
        # Parameters
        self.currency = currency
        self.language = language
        self.product_type = product_type
        self.first_message = first_message
        self.product_terms = open("bot_logic/CD-programs.csv", "r").read()
        self.client_info_str = client_info2string(self.client_info)
        formatted_prompt = self.prompt.format(
            currency=self.currency,
            language = self.language,
            type=self.product_type,
            product_terms=self.product_terms,
            client_info=self.client_info_str,
        )
        self.chat_history.append({
            "role": "system", 
            "content": formatted_prompt
        })
        self.conversation = ""

    def generate_initial_message(self):
        self.chat_history.append(
            {
                "role": "assistant",
                "content": (self.first_message),
            }
        )
        response = self.chat_history[-1]["content"]
        response_to_log = f"Assistant: {response}"
        logging.info(response_to_log)
        self.conversation += response_to_log + "\n"
        return response

    def generate_response(self, user_input: str):
        response_to_log = f"User: {user_input}"
        logging.info(response_to_log)
        self.conversation += response_to_log + "\n"
        start = time.time()
        self.chat_history.append({"role": "user", "content": user_input})
        try:
            self.chat_history, body = get_chat_answer(
                self.chat_history, functions=functions, client_info=self.client_info
            )
            if body:
                self.client_info = body["client_info"]
            response = self.chat_history[-1]["content"]
        except LeavingChat:
            response = "You have left the chat." + "\n"

        end = time.time()
        logging.info(
            f"Time took to generate response: {end - start:.2f} seconds")
        response_to_log = f"Assistant: {response}"
        logging.info(response_to_log)
        self.conversation += response_to_log + "\n"

        self.chat_history[0] = {
            "role": "system",
            "content": self.prompt.format(
                currency=self.currency,
                language = self.language,
                type=self.product_type,
                product_terms=self.product_terms,
                client_info=self.client_info,
            ),
        }

        return response
