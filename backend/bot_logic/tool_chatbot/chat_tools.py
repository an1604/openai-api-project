from typing import Optional, Any
import pickle
import json
from tool_chatbot.utils import (
    INFORMATION_TO_VERIFY,
    get_embedding,
    get_nearest_neighbor,
    get_faq,
    LeavingChat,
    get_products,
    get_time,
    get_time_string,
    WITHDRAWAL_PREFERENCE_MAPPING,
    ChatToolError,
    ClientInfo,
    payout_after_interest,
    client_info2string,
)
import pandas as pd


def assertion_client_info(client_info: ClientInfo) -> ClientInfo:
    try:
        assert isinstance(client_info, ClientInfo)
        assert client_info.amount, "No amount saved in client info."
        assert client_info.duration, "No duration saved in client info."
        assert client_info.credit_score, "No credit score saved in client info."
        assert client_info.monthly_income, "No monthly income saved in client info."
        assert client_info.employment_status, "No employment status saved in client info."
        assert client_info.duration, "No duration saved in client info."
        return True
    except AssertionError:
        return False


def save_client_info(client_info: ClientInfo,
                     amount: Optional[float] = None,
                     duration: Optional[float] = None,
                     credit_score: Optional[int] = None,
                     monthly_income: Optional[float] = None,
                     employment_status: Optional[str] = None,
                     existing_debt: Optional[float] = None,
                     down_payment: Optional[float] = None,
                     dumping_type: Optional[str] = "json"
                     ):
    products = get_products()
    products.columns = products.columns.str.lower()
    products.columns = products.columns.str.replace(' ', '_')
    invalid_values = []
    for item in ("amount", "duration", "credit_score", "monthly_income", "employment_status", "existing_debt",
                 "down_payment"):
        val = eval(item)
        if val:
            set_val = True
            if item in INFORMATION_TO_VERIFY:
                if item == "duration":
                    value_to_verify = get_time_string(val)
                else:
                    value_to_verify = val
                if value_to_verify not in products[item].to_list():
                    invalid_values.append(
                        f"{val} is an invalid value for {item}; Optional values are {products[item].to_list()}")
                    set_val = False
            if set_val:
                setattr(client_info, item, val)
    if invalid_values:
        return f"There were problems with saving client info {'; '.join(invalid_values)}", {"client_info": client_info}
    return f"Client info saved successfully. ({client_info})", {"client_info": client_info}


def get_client_info(validate=True, as_object=False, dumping_type="json"):
    '''Get client info'''
    if dumping_type == "json":
        client_info = ClientInfo(**json.load(open("bot_logic/client_info.json", "r")))
    else:
        client_info = pickle.load(open("bot_logic/client_info.pkl", "rb"))
    if as_object:
        return client_info
    return (
        f"Amount: {client_info.amount}\n"
        f"Duration: {client_info.duration}\n"
        f"Credit Score: {client_info.credit_score}\n"
        f"Monthly Income: {client_info.monthly_income}\n"
        f"Employment Status: {client_info.employment_status}\n"
        f"Existing Debt: {client_info.existing_debt}\n"
        f"Down Payment: {client_info.down_payment}\n"
    )


def create_loan(client_info):
    if assertion_client_info(client_info):
        return "Redirect customer to www.leumi.co.il where they will be able to get a loan."
    return ("You can not have a loan according to your information. Please contact the supporting team for more "
            "details .")


def query_knowledgebase(question, **kwargs):
    """Query the knowledgebase based on chat context.

    Args:
        question (str): Question to ask the knowledgebase."""
    faq = get_faq()
    # Get the embedding for the question
    question_embedding = get_embedding(question)
    # Get the nearest neighbor
    indices, distances = get_nearest_neighbor(question_embedding)
    # Get the FAQ index
    faq_index = indices
    # Get the FAQ answer
    answer = ''
    for i in faq_index:
        if faq[i] == "activate function: get_product_terms":
            answer += get_product_terms()
            answer += "\n"
        else:
            answer += faq[i] + "\n"
    return f'Question: "{question}"\nAnswer: {answer}'


def calculate_interest(program, principal, client_info, **kwargs):
    """Calculate interest based on the given parameters.

    Args:
        product (str): Product name.
        principal (float): Principal investment amount.
    """
    products = pd.read_csv("bot_logic/CD-programs.csv", sep=",").set_index("Program Name")
    try:
        product_terms = products.loc[program]
    except KeyError:
        return f"Could not find programs '{program}'. Only use programs from 'get_recommended_products'"
    # Parse 0.5% to 0.005
    interest_rate = product_terms['APY Rate']
    interest_rate = float(interest_rate[:-1]) / 100
    try:
        time = get_time(product_terms['Duration'])
    except ValueError:
        return "There was an issue with the database. Please contact a human representative."
    total_amount = payout_after_interest(principal, interest_rate, time)
    output = f"{program} Calculation: {principal} (Deposit) * (1 + {interest_rate} (Interest Rate) / 1 (Compounding Frequency)) * {time} (Time in Years)) = {total_amount} (Total Amount). Return: {round(total_amount - principal, 2)}."
    # If the principal amount does not match the amount saved in client info
    # Remind the model to update the client info
    if client_info.amount != principal:
        output += f"\nPrincipal amount does not match the amount saved in client info. Client info: {client_info2string(client_info)}"
    return output


def request_human_rep(request_human_rep=None,
                      **kwargs):  # Placeholders are not used but necessary for the function definition of OpenAI
    """Request human representative"""
    raise LeavingChat


def get_available_durations(get_terms=None, **kwargs):
    """Get available durations for the given product."""
    products = pd.read_csv("bot_logic/CD-programs.csv", sep=",")
    durations = products["Duration"].unique().tolist()
    durations = "\n".join([f"{i + 1}. {x}" for i, x in enumerate(durations)])
    return durations


def get_product_terms(field='all', **kwargs):
    """Get product terms"""
    try:
        if field == 'all':
            product_terms = open("bot_logic/CD-programs.csv", "r").read()
        else:
            if field == 'Program Name':
                product_terms = ','.join(pd.read_csv("bot_logic/CD-programs.csv", sep=",")[field].unique().tolist())
            else:
                # Return field and Program Names
                product_terms = (
                    pd.read_csv("bot_logic/CD-programs.csv", sep=",")
                    .set_index("Program Name")[field]
                    .to_dict()
                )
                product_terms = "\n".join(
                    [f"{k}: {v}" for k, v in product_terms.items()]
                )
    except KeyError as e:
        raise ChatToolError(f"KeyError: {e}")
    return product_terms


def get_recommended_products(return_all=None, client_info=None, **kwargs):
    """Get recommended products based on saved client info"""
    # Assert that at least one relevant client info property is present
    # if not (client_info.duration or client_info.withdrawal_preference):
    #     return "Either duration or withdrawal_preference must be saved in client info."
    # Get all products
    products = pd.read_csv("bot_logic/CD-programs.csv", sep=",")
    # Filter by duration
    if client_info.duration:
        products = products[products["Duration"] == get_time_string(client_info.duration)]
    # Filter by withdrawal preference
    if client_info.withdrawal_preference:
        products = products[
            products["Withdrawal Option"]
            == WITHDRAWAL_PREFERENCE_MAPPING[client_info.withdrawal_preference]
            ]
    if products.empty:
        return "No products found that fit the currently saved client info."
    # Return all products
    product_terms = products.to_dict(orient="records")
    product_terms = "\n".join([f"{row}" for row in product_terms])
    return product_terms


def get_required_documents(get_documents, client_info, **kwargs):
    """Get required documents for opening an account."""
    if assertion_client_info(client_info):
        return "All necessary information is already saved in client info."
    return "Not all required parameters saved in client info"
