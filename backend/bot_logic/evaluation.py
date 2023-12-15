import copy
import random
import json
import pandas as pd
from tool_chatbot import eval
from bot_logic.tool_chatbot.chat_utils import chat_completion_request
from bot_logic.tool_chatbot.chatbot_wrapper import ChatBot
from bot_logic.tool_chatbot.utils import LeavingChat, get_time, WITHDRAWAL_PREFERENCE_MAPPING, get_bot_configuration


def load_prompt(file_path, **params):
    with open(file_path, "r") as f:
        prompt_template = f.read()
    return prompt_template.format(**params)


def run_single_chat(session_config):
    bot = ChatBot(prompt=session_config["prompt_path"], **get_bot_configuration())
    bot.generate_initial_message()
    count = 0
    while count < 10:  # Max 10 turns
        chat_history = bot.chat_history.get_window()
        print("Assistant: " + chat_history[-1]["content"])
        if any(["www.leumi.co.il" in x["content"] for x in chat_history]):
            break
        tester_chat_history = eval.switch_roles(
            copy.deepcopy(chat_history), session_config["tester_prompt"]
        )
        response = chat_completion_request(
            tester_chat_history, [], function_call="none", temperature=0.7
        )
        print("User: " + response.choices[0].message.content)
        try:
            bot.generate_response(response.choices[0].message.content)
        except LeavingChat:
            break
        count += 1
    return bot.chat_history.get_window()


def evaluate_chat_results(chat_history, session_config):
    account_open = eval.account_opened(chat_history)
    is_forgetting = eval.is_not_forgetting_clientinfo(chat_history)
    products = pd.read_csv("bot_logic/CD-programs.csv", sep=",")
    products = products.set_index("Program Name")
    best_product = products.query("Duration == @session_config['duration']")
    best_product = best_product[
        best_product["Withdrawal Option"] == session_config["withdrawal_preference"]
    ]
    interest = best_product["APY Rate"].values[0]
    interest = float(interest[:-1]) / 100
    duration = get_time(best_product["Duration"].values[0])
    is_interest_correct = eval.is_interest_correct(
        chat_history, int(session_config["amount"]), interest, duration
    )
    not_off_topic = eval.not_off_topic(chat_history)
    not_unnecessary_documents = eval.not_unnecessary_documents(chat_history)
    return {
        "account_open": account_open,
        "is_not_forgetting": is_forgetting,
        "is_interest_correct": is_interest_correct,
        "not_off_topic": not_off_topic,
        "not_unnecessary_documents": not_unnecessary_documents,
        "chat_history": chat_history[1:],
    }


def main(eval_prompt_files):
    session_config = {
        "currency": "USD",
        "type": "Certificate of Deposit",
        "persona": "Bob, accountant from New York in his 30s",
        "special_instructions": "Before opening the account, ask what documents are needed.",
    }

    durations = ["1 year", "2 years", "6 months"]
    withdrawal_preferences = ["monthly", "end_of_term"]
    amounts = ["1000", "5000", "10000"]

    # Initialize a dictionary to hold evaluation results
    evaluation_results = {}

    for prompt_file in eval_prompt_files:
        session_config["prompt_path"] = prompt_file
        # Currently only one persona is setup
        n_runs = 10
        aggregated_results = {
            "account_open": [],
            "is_not_forgetting": [],
            "is_interest_correct": [],
            "not_off_topic": [],
            "not_unnecessary_documents": [],
        }

        for run in range(n_runs):
            # Sample a random configuration
            session_config["duration"] = random.choice(durations)
            session_config["withdrawal_preference"] = WITHDRAWAL_PREFERENCE_MAPPING[
                random.choice(withdrawal_preferences)
            ]
            session_config["amount"] = random.choice(amounts)
            session_config["tester_prompt"] = load_prompt(
                "bot_logic/prompts/test_persona.txt", **session_config
            )
            chat_history = run_single_chat(session_config)
            eval_results = evaluate_chat_results(chat_history, session_config)
            for key in aggregated_results.keys():
                if eval_results[key] is not None:
                    aggregated_results[key].append(eval_results[key])
            # Save results
            eval_results["chat_history"] = chat_history
            with open(f"logs/run_{run}.json", "w") as f:
                json.dump(eval_results, f)

        for key in aggregated_results.keys():
            aggregated_results[key] = sum(aggregated_results[key]) / len(
                aggregated_results[key]
            )
        # Store aggregated results in evaluation_results
        evaluation_results[prompt_file] = aggregated_results

    # The evaluation_results dictionary contains all evaluation results keyed by prompt_file
    print("Evaluation Results:", evaluation_results)
    # Save evaluation results to disk
    with open("bot_logic/evaluation_results.json", "w") as f:
        json.dump(evaluation_results, f)


if __name__ == "__main__":
    eval_prompt_files = ["bot_logic/prompts/v4_4.txt"]
    main(eval_prompt_files=eval_prompt_files)
