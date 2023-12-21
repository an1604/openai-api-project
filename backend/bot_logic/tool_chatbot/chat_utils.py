import json

from tool_chatbot.functions import functions
import logging
from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai
import os
from dotenv import load_dotenv
from tool_chatbot.tokens import num_tokens_from_messages, num_tokens_from_functions

from tool_chatbot.exceptions import ChatToolError, MissingArgumentError
from tool_chatbot.utils import get_functions_dict, validate_function_call, _get_tagging_function
from tool_chatbot.prompts import REMEMBER_PROMPT

load_dotenv('.env')

OPENAI_ENGINE = os.getenv('OPENAI_ENGINE')


class ChatMemory(object):
    def __init__(self, token_limit, functions=None):
        self.history = []
        self.token_limit = token_limit
        self.current_token_count = 0 + num_tokens_from_functions(functions)

    def append(self, element):
        new_token_count = num_tokens_from_messages([element])
        self.current_token_count += new_token_count
        self.history.append(element)

        while self.current_token_count > self.token_limit:
            logging.info("Token limit exceeded, removing oldest message")
            removed_element = self.history.pop(1)
            removed_token_count = num_tokens_from_messages([removed_element])
            self.current_token_count -= removed_token_count

    def get_window(self):
        return self.history

    def __getitem__(self, index):
        return self.history[index]

    def __len__(self):
        return len(self.history)

    def __setitem__(self, index, value):
        self.history[index] = value


@retry(
    wait=wait_random_exponential(multiplier=1, max=40),
    stop=stop_after_attempt(3),
    reraise=True,
)
def chat_completion_request(
        messages,
        functions=None,
        function_call="auto",
        engine=OPENAI_ENGINE,
        temperature=0.0,
):
    if isinstance(messages, ChatMemory):
        messages = messages.get_window()

    data = {
        "model": engine,
        "messages": messages,
        "temperature": temperature,
        'max_tokens': os.getenv('MAX_TOKENS')
    }

    if os.getenv("OPENAI_API_TYPE") == "azure":
        data["engine"] = engine

    if functions:
        data["functions"] = functions
        data["function_call"] = function_call

    logging.info('Engine used: "{}"'.format(engine))
    response = openai.ChatCompletion.create(**data)
    return response


def is_client_completed(client):
    return [x is None for x in client.model_dump().values()]


def get_functions_after_remove(functions):
    return [x
            for x in functions
            if x["name"] not in ["calculate_interest", "create_loan"]
            ]


def get_available_functions(response, functions):
    return response.choices[0].message["function_call"]["name"] not in [
        x["name"] for x in functions
    ]


def is_client_info_different(client_info):
    return all([client_info.model_dump()[x] is not None for x in client_info.model_dump().keys()])


def call_function_recursively(history, body, client, response, recursion_depth):
    try:
        history, body = execute_function_call(
            response.choices[0].message,
            history,
            client=client,
            recursion_depth=recursion_depth + 1,
        )
        return history, body
    except ChatToolError as e:
        history.append(
            {
                "role": "function",
                "name": response.choices[0].message["function_call"]["name"],
                "content": f"Error when calling the function: {e}",
            }
        )
    except MissingArgumentError as e:
        history.append(
            {
                "role": "function",
                "name": response.choices[0].message["function_call"]["name"],
                "content": f"Error when calling the function: {e}",
            }
        )
        return history, body


def is_message_contains_in(response):
    return response.choices[0].message.get("content")


def get_missing_arguments_from_function(client_info):
    return [x
            for x in client_info.model_dump().keys()
            if client_info.model_dump()[x] is None
            ]


def function_contains_in(response):
    return response.choices[0].message.get("function_call")


def get_chat_answer(history, functions, client, recursion_depth=0):
    body = None
    if recursion_depth < 5:
        if is_client_completed(client):
            functions = get_functions_after_remove(functions)
        response = chat_completion_request(
            history.get_window(), functions=functions)
    else:
        response = chat_completion_request(
            history.get_window())
    # If function-> call function, get results, generates new answer
    if function_contains_in(response):

        if get_available_functions(response, functions):
            # Currently not allowed to call these functions
            history.append(
                {
                    "role": "function",
                    "name": response.choices[0].message["function_call"]["name"],
                    "content": "Before calling this function, client info must be complete. Missing: {}".
                    format(get_missing_arguments_from_function(client)),
                }
            )
            response = chat_completion_request(history.get_window(
            ), functions=functions, function_call={"name": "save_client_info"})
            if is_client_info_different(client):
                history, body = call_function_recursively(history, body, client, response, recursion_depth)
            else:
                history, body = get_chat_answer(
                    history,
                    functions=functions,
                    client=client,
                    recursion_depth=recursion_depth + 1,
                )
        else:
            function_name = response.choices[0].message["function_call"]["name"]
            history, body = call_function_recursively(history, body, client, response, recursion_depth)
            response = chat_completion_request(history, functions=functions, function_call={"name": function_name})

    elif is_message_contains_in(response):
        logging.info("No function call")
        history.append(
            {
                "role": "assistant",
                "content": response.choices[0].message.content,
            }
        )
    else:
        raise ValueError
    return history, body


def execute_function_call(message, history, client=None, recursion_depth=0):
    body = None
    functions_ref = get_functions_dict()
    validate_function_call(message, functions)

    logging.info('Executing function "{}"'.format(
        message["function_call"]["name"]))
    logging.info('With arguments "{}"'.format(
        message["function_call"]["arguments"]))
    function_output = functions_ref[message["function_call"]["name"]](
        **json.loads(message["function_call"]["arguments"]), client=client
    )

    if isinstance(function_output, tuple):
        function_output, body = function_output[0], function_output[1]
    logging.info('Output "{}"'.format(function_output))
    history.append(
        {
            "role": "function",
            "name": message["function_call"]["name"],
            "content": str(function_output),
        }
    )
    history, body = get_chat_answer(
        history,
        functions=functions,
        client=body["client_info"] if body else client,
        recursion_depth=recursion_depth,
    )
    return history, body


def checks_validate_function_call(answer, function):
    try:
        validate_function_call(answer.choices[0].message, [function])
        return True
    except ChatToolError:
        logging.info(
            "Information Extraction function call not valid, "
            f'arguments: {answer.choices[0].message["function_call"]["arguments"]}'
        )
        return False


def extract_information(received_answer, pydantic_schema):
    PROMPT = """ Extract the customers information for the car loan from the following passage.
    
                Only extract the properties mentioned in the 'information_extraction' function.
                You can leave fields empty if they are not mentioned in the passage.
                
                Passage:
                {passage}
            """
    openai_schema = pydantic_schema.model_json_schema()
    function = _get_tagging_function(openai_schema)

    prompt = PROMPT.format(passage=received_answer)
    history = [{"role": "system", "content": prompt}]
    answer = chat_completion_request(
        history, functions=[function], function_call={"name": function["name"]}
    )

    if not checks_validate_function_call(answer, function):
        return None
    answer = json.loads(answer.choices[0].message["function_call"]["arguments"])

    # If all answers empty, return None
    if not any(answer.values()):
        return None

    logging.info(
        f"Information Extraction function call valid, arguments: {answer}")
    # Create an object from schema
    return pydantic_schema(**answer)
