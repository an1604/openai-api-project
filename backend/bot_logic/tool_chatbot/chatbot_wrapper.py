"""In this module, we define a class that represents the chatbot itself as an object"""

import openai
import os
import dotenv
import logging
import time

from tool_chatbot.exceptions import LeavingChat
from tool_chatbot.Loan_Process.Client.clientInfo import ClientInfo
from tool_chatbot.Loan_Process.Client.client import Client
from tool_chatbot.chat_utils import ChatMemory, get_chat_answer
from tool_chatbot.functions import functions
from tool_chatbot.prompts import (CLIENT_INFO_PROMPT, END_OF_PROMPT_EDITION, ROLE, GENERAL_CONVERSATION,
                                  PROMPT_TEMPLATE, ROLE_TEMPLATE, CONTEX_TEMPLATE)
from tool_chatbot.helper_functions import get_text_from_file

dotenv.load_dotenv()


def generate_user_prompt(user_input, currency, language, client):
    role_text = 'Role: {}'.format(ROLE)
    contex_text = CONTEX_TEMPLATE.format(user_input)
    prompt_text = PROMPT_TEMPLATE.format(role_text, contex_text, CLIENT_INFO_PROMPT, END_OF_PROMPT_EDITION)

    return prompt_text.format(
        currency=currency,
        language=language,
        client=client
    )


class ChatBot:
    def __init__(self,
                 currency: str,
                 language: str,
                 first_message: str,
                 product_terms_path='bot_logic/CL-programs.csv',
                 prompt_path="bot_logic/prompts/v4_1ofer.txt") -> None:
        assert os.getenv(
            "OPENAI_API_KEY"
        ), "Please set your OPENAI_API_KEY environment variable."
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.client = Client.initiate_client(dump=False)
        self.chat_history = ChatMemory(token_limit=3896, functions=functions)
        self.prompt = get_text_from_file(prompt_path)

        # Params:
        self.currency = currency
        self.language = language
        self.first_message = first_message
        self.product_terms = get_text_from_file(product_terms_path)
        self.client_str = self.client.client_to_string()

        formatted_prompt = self.prompt.format(
            currency=self.currency,
            language=self.language,
            client_info=self.client_str,
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

    def get_response(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})

        try:
            self.chat_history, body = get_chat_answer(
                self.chat_history, functions=functions, client=self.client
            )
            if body:
                self.client = body["client"]
            response = self.chat_history[-1]["content"]
        except LeavingChat:
            response = "You have left the chat." + "\n"

        return response

    def generate_response(self, user_input: str) -> str:
        user_prompt = generate_user_prompt(user_input, self.currency, self.language, self.client)
        response_to_log = f"User: {user_prompt}"
        logging.info(response_to_log)
        self.conversation += response_to_log + "\n"

        # Calculate the overall time to get the response
        start = time.time()
        response = self.get_response(user_prompt)
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
                language=self.language,
                client_info=self.client,
            ),
        }

        return response
