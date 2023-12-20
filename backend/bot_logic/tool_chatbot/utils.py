"""In this module we define all the utility functions of the model"""
import os
import time

import numpy as np
import faiss
import openai
import pandas as pd
import logging
import json
from typing import Optional

from openai.error import RateLimitError
import inspect

from tool_chatbot.exceptions import ChatToolError, MissingArgumentError


# Getting the car loan products
def get_products(path: str, sep: str, set_index: Optional[bool] = None):
    products = pd.read_csv(path, sep=sep)
    if set_index:
        products = products.set_index(["Duration"])
    return products


def get_faq():
    df = pd.read_csv("bot_logic/knowledgebase.csv", sep=";")
    faq = [x + " - " + y for x, y in df.values]
    return faq


def get_embedding_response(text):
    try:
        return openai.Embedding.create(input=text, engine="text-embedding-ada-002")
    except RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
        print(f"Waiting for 20 seconds before retrying...")
        return None


def get_embedding(text):
    """Get the embedding for a given text. Returns a numpy array of shape (1, vectorDim)."""
    counter = 0
    while counter < 3:
        response = get_embedding_response(text)
        if response is not None:
            print('Done.')
            return np.array(response.data[0].embedding).reshape(1, -1)
        time.sleep(20)


def get_nearest_neighbor(vector, index_file="bot_logic/vector_index.faiss", k=3):
    """
        Fetches the nearest neighbor of a given vector from a FAISS index.

        Parameters:
            vector (numpy.ndarray): The query vector.
            index_file (str): Path to the saved FAISS index file.
            k (int): Number of the nearest neighbors to fetch.

        Returns:
            tuple: Indices and distances of the nearest neighbors.
        """
    index = faiss.read_index(index_file)
    query_vector = vector.astype("float32")
    distances, indices = index.search(query_vector, k)
    return indices, distances


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
    """Returns a string with the duration in months"""
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
        duration_string = f"{val} months"
        if duration == 1:
            duration_string = duration_string[:-1]
    return duration_string


def _convert_schema(schema: dict) -> dict:
    properties = {k: {"title": k, **v} for k, v in schema["properties"].items()}
    return {
        "type": "object",
        "properties": properties,
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
            'first_message': "היי מה שלומך? ברוכים הבאים לעוזר האישי בנושא מימון לרכב! "
                             ", האם תרצה לשמוע עוד פרטים?"
        },
        'english': {
            'currency': "USD",
            'language': "English",
            'first_message': "Hi, how are you? Welcome to the car loans assistance!  Would you like to hear more "
                             "about the terms of the loans or even just hear a little bit about car loans at all??"
        }
    }

    CURRENT_LANGUAGE = os.getenv("CURRENT_LANGUAGE") or "english"
    return configurations[CURRENT_LANGUAGE]