"""For cleaner files, the 'helper functions' are in a different file"""
import re

import joblib
import numpy as np
import pandas as pd

from tool_chatbot.Loan_Process.Client.clientInfo import ClientInfo, INFORMATION_TO_VERIFY
from tool_chatbot.utils import get_time, get_products, get_time_string
from tool_chatbot.Loan_Process.Client.client import Client
from tool_chatbot.Loan_Process.Products_Predictions.model_params import classifier, sc, ct


def get_text_from_file(path):
    with open(path, "r") as f:
        return f.read()


# Get the product terms from a specific program
def get_terms(products, program):
    try:
        return products.loc[program]
    except KeyError:
        return None


def try_to_get_time(param):
    try:
        return get_time(param)
    except ValueError:
        return -1


def get_available_products(loan_amount, duration, down_payment):
    products = get_products(path='bot_logic/CL-programs.csv', sep=',')
    products.columns = products.columns.str.lower()
    products.columns = products.columns.str.replace(' ', '_')
    invalid_values = []
    for item in ("duration", "down_payment", "loan_amount"):
        val = locals().get(item)
        if item in INFORMATION_TO_VERIFY:
            if item == "duration":
                value_to_verify = get_time_string(val)
            else:
                value_to_verify = val
        if value_to_verify not in products[item].to_list():
            invalid_values.append(
                f"{val} is an invalid value for {item}; Optional values are {products[item].to_list()}")

    if invalid_values:
        return (
            f"There is an invalid values, and you can not get a specific loan, The invalided values are:  {invalid_values}."
            f"Call `get_recommended_products` function to get a list of suitable products.")

    return "Successfully found an available car loan, you can get a specific loan."


def predict_suitable_products(prediction):
    return classifier.predict(prediction)


def generate_prediction_format(client: Client):
    prediction_format = {
        'Employee_Status': client.get_client_personal_info().employment_status.lower(),
        'Duration': client.get_client_info().duration,
        'Loan Amount': client.get_client_info().loan_amount,
        'Down_payment': client.get_client_info().down_payment_status,
        'Annual_income': client.get_client_personal_info().annual_income
    }

    prediction_df = pd.DataFrame([prediction_format])
    prediction_df['Employee_Status'] = prediction_df['Employee_Status'].str.lower()
    prediction_after_ct = ct.transform(prediction_df)
    prediction_after_ct = prediction_after_ct[:, 1:]
    prediction = pd.DataFrame(prediction_after_ct,
                              columns=['Employee_Status', 'Duration', 'Loan Amount', 'Down_payment', 'Annual_income'])
    prediction.iloc[:, 1:] = sc.transform(prediction.iloc[:, 1:])
    y_prediction = np.array(prediction)
    return y_prediction


def extract_float_from_string(value_str):
    match = re.search(r'[\d,]+(\.\d+)?', value_str)

    if match and match.group(0) is not None:
        cleaned_value = match.group(0).replace(',', '')
        return float(cleaned_value)
    else:
        return -1



