import os
import time

import numpy as np
import faiss
import openai
import pandas as pd
import logging
import json
import pickle
from typing import Optional

from openai.error import RateLimitError
from pydantic import Field
from pydantic import BaseModel
import inspect


# Create new Exception class
class LeavingChat(Exception):
    """Exception raised when the user wants to leave the chat."""

    pass


class ChatToolError(Exception):
    """Exception raised when an error occurs when calling the chat tools."""

    pass


class MissingArgumentError(Exception):
    """Exception raised when a required argument is missing."""

    pass


class ClientInfo(BaseModel):
    """Client information."""

    amount: Optional[int] = Field(
        ...,
        ge=0,
        description="Amount they wish to deposit (P).",
    )
    duration: Optional[float] = Field(
        ...,
        ge=0,
        # TODO we could add a maximum duration
        description="Duration of deposit (t in years).",
    )
    withdrawal_preference: Optional[str] = Field(
        ...,
        enum=["end_of_term", "monthly"],
        description=(
            "Withdrawal preference (if the customer wants access to their money "
            "end of the term or every month). Only valid options are 'end_of_term' "
            "and 'monthly'."
        ),
    )


WITHDRAWAL_PREFERENCE_MAPPING = {
    "monthly": "Every month",
    "end_of_term": "End of term",
}

INFORMATION_TO_VERIFY = ["duration", "withdrawl_preference"]


def get_products(path: str = "bot_logic/CD-programs.csv", sep: str = ",", set_index: Optional[bool] = None):
    products = pd.read_csv(path, sep=sep)
    if set_index:
        products = products.set_index(["Duration", "Withdrawal Option"])
    return products


def initiate_client_info():
    # Setup storage for Client Info
    client_info = ClientInfo(
        amount=None,
        duration=None,
        withdrawal_preference=None,
    )
    # Save as JSON
    with open("client_info.json", "w") as f:
        json.dump(client_info.model_dump(), f)
    return client_info


def client_info2string(client_info):
    return (
        f"\tAmount: {client_info.amount}\n"
        f"\tDuration: {client_info.duration}\n"
        f"\tWithdrawal Preference: {client_info.withdrawal_preference}"
    )


def get_faq():
    """Get the FAQ from the knowledgebase."""
    df = pd.read_csv("bot_logic/knowledgebase.csv", sep=";")
    faq = [x + " - " + y for x, y in df.values]
    return faq


def get_embedding(text):
    """Get the embedding for a given text. Returns a numpy array of shape (1, vectorDim)."""
    counter = 0
    while counter < 3:
        try:
            counter += 1
            response = openai.Embedding.create(input=text, engine="text-embedding-ada-002")
            print('Done.')
            return np.array(response.data[0].embedding).reshape(1, -1)
        except RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
            print(f"Waiting for 20 seconds before retrying...")
            time.sleep(20)
    raise RateLimitError("Max retries exceeded.")


def get_nearest_neighbor(vector, index_file="bot_logic/vector_index.faiss", k=3):
    """
    Fetches the nearest neighbor of a given vector from a FAISS index.

    Parameters:
        vector (numpy.ndarray): The query vector.
        index_file (str): Path to the saved FAISS index file.
        k (int): Number of nearest neighbors to fetch.

    Returns:
        tuple: Indices and distances of the nearest neighbors.
    """

    # Load the FAISS index from the file
    index = faiss.read_index(index_file)

    # Make sure the query vector is in float32 format
    query_vector = vector.astype("float32")

    # Perform the search
    distances, indices = index.search(query_vector, k)

    return indices[0], distances[0]


def get_functions_dict():
    import tool_chatbot.chat_tools

    functions = inspect.getmembers(tool_chatbot.chat_tools, inspect.isfunction)
    functions = {name: function for name, function in functions}
    return functions


def get_time(duration_string):
    """Returns a float with the duration in years"""
    if "month" in duration_string:
        duration = float(duration_string.split(" ")[0]) / 12
    elif "year" in duration_string:
        duration = float(duration_string.split(" ")[0])
    else:
        raise ValueError("Duration string not recognized.")
    return duration


def get_time_string(duration):
    """Returns a string with the duration in years"""
    if duration < 1:
        if duration * 12 == int(duration * 12):
            duration_string = f"{int(duration * 12)} months"
        else:
            duration_string = f"{duration * 12} months"
    else:
        if float(duration) == int(duration):
            val = int(duration)
        else:
            val = float(duration)
        duration_string = f"{val} years"
        if duration == 1:
            duration_string = duration_string[:-1]
    return duration_string


def _convert_schema(schema: dict) -> dict:
    props = {k: {"title": k, **v} for k, v in schema["properties"].items()}
    return {
        "type": "object",
        "properties": props,
        "required": schema.get("required", []),
    }


def _get_tagging_function(schema: dict) -> dict:
    return {
        "name": "information_extraction",
        "description": "Extracts the relevant information from the passage.",
        "parameters": _convert_schema(schema),
    }


def validate_function_call(message, functions):
    try:
        function_schema = [
            x for x in functions if x["name"] == message["function_call"]["name"]
        ][0]
        args = json.loads(message["function_call"]["arguments"])
        assert all(
            [
                x in args
                for x in function_schema["parameters"].get("required", [])
            ]
        )
    except json.decoder.JSONDecodeError as e:
        logging.info("Issue with JSON decoding")
        raise ChatToolError(e)
    except IndexError as e:
        logging.info('Function "{}" not found'.format(message["function_call"]["name"]))
        raise ChatToolError(e)
    except AssertionError as e:
        logging.info(
            'Not all required parameters for function "{}" were provided. These are the required parameters: {}'.format(
                message["function_call"]["name"],
                function_schema["parameters"].get("required", []),
            )
        )
        raise MissingArgumentError(e)


def payout_after_interest(principal, interest_rate, time):
    total_amount = principal * (1 + interest_rate / 1) ** (
            1 * time
    )
    return round(total_amount, 2)


def dump_client_info(client_info, dumping_type):
    if dumping_type == "dynamic":
        return
    elif dumping_type == "json":
        with open("bot_logic/client_info.json", "w") as f:
            json.dump(client_info.model_dump(), f)
    elif dumping_type == "pickle":
        with open("bot_logic/client_info.pkl", "wb") as f:
            pickle.dump(client_info, f)


def get_log_name(logs_path: str = "bot_logic/logs", fn_prefix: str = "chatbot", fn_suffix: str = "log") -> str:
    log_files = [x for x in os.listdir(logs_path) if f".{fn_suffix}" in x]
    if log_files:
        uuid = max([int(x.split(".")[0].split("_")[-1]) for x in log_files]) + 1
    else:
        uuid = 1
    return f"{fn_prefix}_{uuid}.{fn_suffix}"


def get_bot_configuration():
    configurations = {
        'hebrew': {
            'currency': "Shekel",
            'language': "Hebrew",
            'product_type': "תוכנית חסכון",
            'first_message': "היי מה שלומך? המומחים שלנו בדקו את חשבונך ומצאו שעכשיו יהיה זמן נהדר בשבילך לפתוח תוכנית חסכון, האם תרצה לשמוע עוד פרטים?"
        },
        'english': {
            'currency': "USD",
            'language': "English",
            'product_type': "Certificate of Deposit",
            'first_message': "Hi, how are you? Our experts have checked your account and found that now is a great time for you to open a Certificate of Deposit. Would you like to hear more details?"
        }
    }

    CURRENT_LANGUAGE = os.getenv("CURRENT_LANGUAGE") or "english"
    return configurations[CURRENT_LANGUAGE]
