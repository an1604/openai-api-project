"""In this module, we define the logic for chatbot."""
from typing import Optional

import pandas as pd

from tool_chatbot.exceptions import LeavingChat, ChatToolError
from tool_chatbot.utils import get_faq, get_embedding, get_nearest_neighbor, get_products, get_time, \
    payout_after_interest, get_time_string
from tool_chatbot.Loan_Process.Client.clientInfo import ClientInfo
from tool_chatbot.Loan_Process.Client.client import Client
from .helper_functions import try_to_get_time, get_terms, get_available_products, predict_suitable_products, \
    generate_prediction_format, extract_float_from_string


def check_for_available_products(client: Client,
                                 kwargs: Optional[Client] = None):
    try:
        if Client.assertion_is_valid(client):
            products = get_available_products(down_payment=client.get_client_info().down_payment_status,
                                              duration=client.get_client_info().duration,
                                              loan_amount=client.get_client_info().loan_amount)
            return products
    except AssertionError as e:
        return "Client information is not acceptable. Get the missing information and try again. See what is missing: {}".format(
            e)


def save_client_personal_information(client: Client,
                                     first_name: Optional[str] = None,
                                     last_name: Optional[str] = None,
                                     annual_income: Optional[float] = None,
                                     employment_status: Optional[str] = None,
                                     dumping_type: Optional[str] = "json"):
    if any((first_name, last_name, annual_income, employment_status)):
        if first_name:
            client.get_client_personal_info().first_name = first_name
        if last_name:
            client.get_client_personal_info().last_name = last_name
        if annual_income:
            client.get_client_personal_info().annual_income = annual_income
        if employment_status:
            client.get_client_personal_info().employment_status = employment_status
        return f"Client personal information saved successfully. ({client})"
    else:
        return "No personal information provided for saving."


def save_client_info(client: Client,
                     amount: Optional[float] = None,
                     duration: Optional[float] = None,
                     down_payment_status: Optional[bool] = None,
                     dumping_type: Optional[str] = "json"
                     ):
    if any([amount, duration, down_payment_status]):
        if amount:
            client.get_client_info().loan_amount = amount
        if duration:
            client.get_client_info().duration = duration
        if down_payment_status:
            client.get_client_info().down_payment_status = down_payment_status
        return f"Client financial info saved successfully. ({client.get_client_info()})", {"client_info": client}
    else:
        return "Can not save client financial info without loan amount or duration.", {"client_info": client}


def save_car_details(client: Client,
                     make_and_model: Optional[str] = None,
                     purchase_price: Optional[float] = None,
                     vin: Optional[str] = None,
                     condition: Optional[str] = None):
    if any([make_and_model, purchase_price, vin]):
        if make_and_model:
            client.get_car_details().make_and_model = make_and_model
        if purchase_price:
            client.get_car_details().purchase_price = purchase_price
        if vin:
            client.get_car_details().vin = vin
        if condition:
            client.get_car_details().condition = condition
        return f"Car details saved successfully. ({client.get_car_details()})", {"client_info": client}
    else:
        return "Not enough arguments provided for saving.", {"client_info": client}


def save_loan_details(client: Client,
                      program_name: Optional[str] = None,
                      loan_amount: Optional[str] = None,
                      loan_duration: Optional[str] = None,
                      apy_rate: Optional[str] = None,
                      employed_status: Optional[str] = None,
                      down_payment: Optional[str] = None,
                      annual_income: Optional[str] = None):
    if any([program_name, loan_amount, loan_duration, apy_rate, employed_status, down_payment, annual_income]):
        if program_name:
            client.get_loan().program_name = program_name
        if loan_amount:
            loan_amount = extract_float_from_string(loan_amount)
            if loan_amount > 0:
                client.get_loan().loan_amount = loan_amount
        if loan_duration:
            loan_duration = extract_float_from_string(loan_duration)
            if loan_duration > 0:
                client.get_loan().loan_duration = loan_duration
        if apy_rate:
            apy_rate = extract_float_from_string(apy_rate)
            if apy_rate > 0:
                client.get_loan().apy_rate = apy_rate
        if employed_status:
            client.get_loan().employed_status = employed_status
        if down_payment:
            down_payment = extract_float_from_string(down_payment)
            if down_payment > 0:
                client.get_loan().down_payment = down_payment
        if annual_income:
            annual_income = extract_float_from_string(annual_income)
            if annual_income > 0:
                client.get_loan().annual_income = annual_income

        if 'successfully' in client.get_loan().create_loan():
            return 'Loan successfully created. Ask the client to confirm the following monthly bill:{} . If the client confirms the billing, send this link for the client for next operations: www.leumi.com'.format(
                client.get_loan().monthly_payment)
    return 'Failed to create the loan. Suggest speaking with a human representative for more actions.'


def query_knowledgebase(question, **kwargs):
    faq = get_faq()
    question_embedding = get_embedding(question)
    indices, distances = get_nearest_neighbor(question_embedding)
    faq_index = indices
    faq_answer = ''

    for i in faq_index:
        faq_content = faq[i]

        if faq_content == "activate function: get_product_terms":
            faq_answer += get_product_terms()
            faq_answer += '\n'
        else:
            faq_answer += faq_content + '\n'

    return f'Question: "{question}"\nAnswer: {faq_answer}'


def get_interest_details(program, principal, interest_rate, total_amount, time, client_info=None):
    output = f"{program} Calculation: {principal} (Deposit) * (1 + {interest_rate} (Interest Rate) / 1 (Compounding Frequency)) * {time} (Time in Years)) = {total_amount} (Total Amount). Return: {round(total_amount - principal, 2)}."
    if client_info:
        output += f"\nPrincipal amount does not match the amount saved in client info. Client info: {client_info.client_info2string()},use 'get_recommended_products' function to suggest suitable products for the client."
    return output


def calculate_interest(program, principal, client, **kwargs):
    """Calculate interest based on the given parameters.

        Args:
            product (str): Product name.
            principal (float): Principal investment amount.
    """
    products = get_products(path='bot_logic/CL-programs.csv', sep=',').set_index('Program Name')

    product_terms = get_terms(products, program)
    if product_terms is None:
        return f"Could not find programs '{program}'. use 'get_recommended_products' function to suggest suitable products for the client. "

    # Parse 0.5% to 0.005
    interest_rate = product_terms['APY Rate']
    interest_rate = float(interest_rate[:-1]) / 100

    time = try_to_get_time(product_terms['Duration'])
    if time == -1:
        return "There was an issue with the database. Please contact a human representative."

    total_amount = payout_after_interest(principal, interest_rate, time)
    # Checking If the principal amount does not match the amount saved in client info,
    # and passing client_info if it's true.
    client_info_amount_is_not_principle = client.client_info.amount != principal
    return get_interest_details(program, principal, interest_rate,
                                total_amount, time,
                                client.client_info if client_info_amount_is_not_principle else None)


def request_human_rep(request_human_rep=None,
                      **kwargs):  # Placeholders are not used but necessary for the function definition of OpenAI
    """Request human representative"""
    raise LeavingChat


def get_available_durations(get_terms=None, **kwargs):
    """Get available durations for the given product."""
    products = get_products(path='bot_logic/CL-programs.csv', sep=',')
    durations = products["Duration"].unique().tolist()
    durations = "\n".join([f"{i + 1}. {x}" for i, x in enumerate(durations)])
    return durations


def get_fields_and_program_names(field):
    product_terms = (
        pd.read_csv("bot_logic/CL-programs.csv", sep=",")
        .set_index("Program Name")[field]
        .to_dict()
    )
    product_terms = "\n".join(
        [f"{k}: {v}" for k, v in product_terms.items()]
    )
    return product_terms


def get_product_terms(field='all', **kwargs):
    """Get product terms"""
    try:
        if field == 'all':
            product_terms = open("bot_logic/CL-programs.csv", "r").read()
        else:
            if field == 'Program Name':
                product_terms = ','.join(
                    pd.read_csv("bot_logic/CL-programs.csv", sep=",")[field].unique().tolist())
            else:
                product_terms = get_fields_and_program_names(field)
    except KeyError as e:
        raise ChatToolError(f"KeyError: {e}")
    return product_terms


def get_recommended_products(return_all=None, client=None, **kwargs):
    """Get recommended products based on saved client info"""
    products_df = get_products(path='bot_logic/CL-programs.csv', sep=',')
    products = get_products(path='bot_logic/CL-programs.csv', sep=',')
    # Filter by duration
    if client.client_info.duration:
        products = products[products["Duration"] <= get_time_string(client.client_info.duration)]

    if products.empty:
        client_loan_information = generate_prediction_format(client)  # Trying to find closer suitable product.
        recommended_products = predict_suitable_products(client_loan_information)
        if recommended_products:
            products = products_df.loc[products_df['Program Name'] == recommended_products[0]]

    product_terms = products.to_dict(orient="records")
    product_terms = "\n".join([f"{row}" for row in product_terms])
    return product_terms


def get_required_documents(get_documents, client, **kwargs):
    """Get required documents for taking a loan."""
    if ClientInfo.assertion_client_info(client.client_info):
        return "All necessary information is already saved in client info."

    return "Not all required parameters saved in client info"
