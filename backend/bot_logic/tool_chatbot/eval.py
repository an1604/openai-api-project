import json
from tool_chatbot.chat_utils import chat_completion_request
from tool_chatbot.utils import payout_after_interest


def switch_roles(chat_history, new_system_content):
    new_history = []
    for i in range(len(chat_history)):
        if chat_history[i]["role"] == "user":
            new_history.append(
                {
                    "role": "assistant",
                    "content": chat_history[i]["content"],
                }
            )
        elif chat_history[i]["role"] == "assistant":
            new_history.append(
                {
                    "role": "user",
                    "content": chat_history[i]["content"],
                }
            )
        elif chat_history[i]["role"] == "system":
            new_history.append(
                {
                    "role": "assistant",
                    "content": new_system_content,
                }
            )
        elif chat_history[i]["role"] == "function":
            pass
    return new_history


def stringify_conversation(chat_history):
    conversation = ""
    for i in range(len(chat_history)):
        if chat_history[i]["role"] == "user":
            conversation += "User: " + chat_history[i]["content"] + "\n"
        elif chat_history[i]["role"] == "assistant":
            conversation += "Assistant: " + chat_history[i]["content"] + "\n"
        elif chat_history[i]["role"] == "system":
            pass
    return conversation


eval_functions = [
    {
        "name": "classification",
        "description": "save the classification based on the user query.",
        "parameters": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "boolean",
                    "description": "Classification label",
                }
            },
        },
    }
]


def is_not_forgetting_clientinfo(chat_history):
    # TODO maybe ask if the bot is actually forgetting any specific client info
    """Classify if the bot forgot the client info at any time."""
    FORGETTING_PROMPT = "Here is a chat history between a bot and a user. " \
                        "Did the bot ask for the following information, even though " \
                        "the user has provided them already?\n" \
                        "1. The amount of money the user wants to deposit\n" \
                        "2. The duration of the deposit\n" \
                        "3. The user's withdrawal preference (monthly or end of term)\n" \
                        "Return True if the bot is not forgetting any of the above information, and False otherwise.\n\n" \
                        "\n{conversation}"
    conversation = stringify_conversation(chat_history)
    prompt = FORGETTING_PROMPT.format(conversation=conversation)
    messages = [
        {"role": "system", "content": "You are an helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    output = chat_completion_request(
        messages, eval_functions, function_call={"name": "classification"}
    )
    func_call = json.loads(output.choices[0].message["function_call"]["arguments"])
    return func_call["label"]


def account_opened(chat_history):
    """Check if the user was redirected to the correct website."""
    return any(
        [
            "www.leumi.co.il" in x["content"]
            for x in chat_history
            if x["role"] == "assistant"
        ]
    )


def is_interest_correct(chat_history, principal, interest_rate, duration):
    """Check if the interest rate is returned correctly to the user."""
    if not any(
        [
            "calculate_interest" == x.get("name")
            for x in chat_history
        ]
    ):
        return None
    total_amount = payout_after_interest(
        principal=principal,
        interest_rate=interest_rate,
        time=duration,
    )
    return any(
        [
            (f"{total_amount}" in x["content"]
             or f"{round(principal - total_amount, 2)}" in x["content"]
             or f"{round(total_amount - principal, 0)}" in x["content"]
             or f"{int(total_amount)}" in x["content"])
            for x in chat_history
            if x["role"] == "assistant"
        ]
    )


def not_off_topic(chat_history):
    """Check if the bot is not going off topic."""
    PROMPT = "Here is a chat history between a bot and a user. " \
             "The bot is supposed to help the user open a deposit account and answer the users questions about Leumis banking products" \
             "Return True if the bot is not going off topic, and False otherwise.\n\n" \
             "{conversation}"
    conversation = stringify_conversation(chat_history)
    prompt = PROMPT.format(conversation=conversation)
    messages = [
        {"role": "system", "content": "You are an helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    output = chat_completion_request(
        messages, eval_functions, function_call={"name": "classification"}
    )
    func_call = json.loads(output.choices[0].message["function_call"]["arguments"])
    return func_call["label"]


def not_unnecessary_documents(chat_history):
    """Check if the bot is not going off topic."""
    PROMPT = "Here is a chat history between a bot and a user. " \
             "The bot is supposed to help the user open a deposit account and answer the users questions about Leumis banking products" \
             "Return True if the bot does not say that social security, email, proof of identity or similar are required.\n\n" \
             "{conversation}"
    conversation = stringify_conversation(chat_history)
    prompt = PROMPT.format(conversation=conversation)
    messages = [
        {"role": "system", "content": "You are an helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    output = chat_completion_request(
        messages, eval_functions, function_call={"name": "classification"}
    )
    func_call = json.loads(output.choices[0].message["function_call"]["arguments"])
    return func_call["label"]
