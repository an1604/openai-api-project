import json
from bot_logic.tool_chatbot.functions import functions
import logging
from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai
import os
from dotenv import load_dotenv
from bot_logic.tool_chatbot.utils import (
    MissingArgumentError,
    ChatToolError,
    get_functions_dict,
    validate_function_call,
    _get_tagging_function,
)
from bot_logic.tool_chatbot.tokens import num_tokens_from_messages, num_tokens_from_functions


REMEMBER_PROMPT = {"role": "system", "content": open(
    "bot_logic/prompts/remember.txt", "r").read()}

load_dotenv('.env')
OPENAI_ENGINE = os.getenv('OPENAI_ENGINE')


class ChatMemory:
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
            removed_element = self.history.pop(1)  # Don't remove the prompt
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
    }
    if os.getenv("OPENAI_API_TYPE") == "azure":
        data["engine"] = engine
    if functions:
        data["functions"] = functions
        data["function_call"] = function_call
    logging.info('Engine used: "{}"'.format(engine))
    response = openai.ChatCompletion.create(**data)
    return response


def get_chat_answer(history, functions, client_info, recursion_depth=0):
    body = None
    if recursion_depth < 5:
        # If client info isn't complete, remove functions that require it
        if any([x is None for x in client_info.model_dump().values()]):
            # Remove functions that require client info
            functions = [
                x
                for x in functions
                if x["name"] not in ["calculate_interest", "open_account"]
            ]
        response = chat_completion_request(
            history.get_window() + [REMEMBER_PROMPT], functions=functions)
    else:
        response = chat_completion_request(
            history.get_window() + [REMEMBER_PROMPT])
    # If function, call function, get results, generate new answer
    if response.choices[0].message.get("function_call"):
        # Testing if function is in available functions
        if response.choices[0].message["function_call"]["name"] not in [
            x["name"] for x in functions
        ]:
            # Currently not allowed to call these functions
            history.append(
                {
                    "role": "function",
                    "name": response.choices[0].message["function_call"]["name"],
                    "content": "Before calling this function, client info must be complete. Missing: {}".format(
                        [
                            x
                            for x in client_info.model_dump().keys()
                            if client_info.model_dump()[x] is None
                        ]
                    ),
                }
            )
            response = chat_completion_request(history.get_window(
            ) + [REMEMBER_PROMPT], functions=functions, function_call={"name": "save_client_info"})
            # Compare if client_info is different
            if all([client_info.model_dump()[x] is not None for x in client_info.model_dump().keys()]):
                # If client info is complete, call the function
                history, body = execute_function_call(
                    response.choices[0].message,
                    history,
                    client_info=client_info,
                    recursion_depth=recursion_depth + 1,
                )
            else:
                history, body = get_chat_answer(
                    history,
                    functions=functions,
                    client_info=client_info,
                    recursion_depth=recursion_depth + 1,
                )
        else:
            try:
                history, body = execute_function_call(
                    response.choices[0].message,
                    history,
                    client_info=client_info,
                    recursion_depth=recursion_depth + 1,
                )
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
                response = chat_completion_request(history, functions=functions, function_call={
                                                   "name": response.choices[0].message["function_call"]["name"]})

    # If message, return message
    elif response.choices[0].message.get("content"):
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


def execute_function_call(message, history, client_info=None, recursion_depth=0):
    body = None
    functions_ref = get_functions_dict()
    validate_function_call(message, functions)
    logging.info('Executing function "{}"'.format(
        message["function_call"]["name"]))
    logging.info('With arguments "{}"'.format(
        message["function_call"]["arguments"]))
    function_output = functions_ref[message["function_call"]["name"]](
        **json.loads(message["function_call"]["arguments"]), client_info=client_info
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
        client_info=body["client_info"] if body else client_info,
        recursion_depth=recursion_depth,
    )
    return history, body


def extract_information(received_answer, pydantic_schema):
    PROMPT = """Extract the customers information for the Certificate of Deposit product from the following passage.

                Only extract the properties mentioned in the 'information_extraction' function.
                If the customer wants to keep access to their money, you should choose 'monthly'.
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
    try:
        validate_function_call(answer.choices[0].message, [function])
    except ChatToolError:
        logging.info(
            "Information Extraction function call not valid, "
            f'arguments: {answer.choices[0].message["function_call"]["arguments"]}'
        )
        return None
    answer = json.loads(
        answer.choices[0].message["function_call"]["arguments"])
    # If all answers empty, return None
    if not any(answer.values()):
        return None
    logging.info(
        f"Information Extraction function call valid, arguments: {answer}")
    # Create object from schema
    return pydantic_schema(**answer)
