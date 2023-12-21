functions = [
    {
        "name": "save_client_info",
        "description": "Save client info. This needs to be called always when the client provides new information or when he updates his information. ",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "Amount they wish to deposit (P)."
                },
                "duration": {
                    "type": "number",
                    "description": "Duration of deposit in years. Use float for months or weeks (e.g. 0.5 for 6 months)."
                }
            },
            "required": []
        }
    },
    {
        "name": "save_car_details",
        "description": "Save car details according to the information provided. This needs to be called always when the client provides new information about his car or when he updates his information.",
        "parameters": {
            "type": "object",
            "properties": {
                "make_and_model": {
                    "type": "string",
                    "description": "The car make and model name. (e.g 'Toyota Camry', 'San Francisco')"
                },
                "purchase_price": {
                    "type": "number",
                    "description": "The car purchase price. Use float for months or weeks (e.g for 6 months)."
                },
                "vin": {
                    "type": "string",
                    "description": "The vehicle identification number of the car (e.g '12345678901234567').Use a long string for car identification."
                }
            },
            "required": ["make_and_model", "purchase_price", "vin"]
        }
    },
    {
        "name": "save_client_personal_information",
        "description": "Save client personal information according to the personal information provided by the client. This needs to be called at the beginning of the conversation process to get information about the client, and before continuing to the financial details and the loan process.",
        "parameters": {
            "type": "object",
            "properties": {
                "first_name": {
                    "type": "string",
                    "description": "The first name of the client."
                },
                "last_name": {
                    "type": "string",
                    "description": "The last name of the client."
                },
                "annual_income": {
                    "type": "number",
                    "description": "The annual income of the client. Use float to accurately represent the annual income."
                },
                "employment_status": {
                    "type": "string",
                    "description": "The employment status of the client. Use strings to indicate the employment status. (e.g 'employed', 'self-employed')"
                }
            },
            "required": ["first_name", "last_name", "employment_status", "annual_income"]
        }
    },
    {
        "name": "query_knowledgebase",
        "description": "Query the knowledgebase to answer a general question about the products. The question should be formulated in a way that no further context is required to answer it.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Question to ask the knowledgebase."
                }
            },
            "required": ["question"]
        }
    },
    {
        "name": "calculate_interest",
        "description": "Calculate the total amount after interest based on a recommended program.",
        "parameters": {
            "type": "object",
            "properties": {
                "principal": {
                    "type": "number",
                    "description": "Principal amount (P)."
                },
                "program": {
                    "type": "string",
                    "description": "Name of the recommended program."
                }
            },
            "required": ["principal", "program"]
        }
    },
    {
        "name": "request_human_rep",
        "description": "Request a human representative",
        "parameters": {
            "type": "object",
            "properties": {
                "request_human_rep": {
                    "type": "boolean",
                    "description": "Request a human representative."
                }
            }
        }
    },
    {
        "name": "get_product_terms",
        "description": "Call this function to retrieve product details.",
        "parameters": {
            "type": "object",
            "properties": {
                "return_all": {
                    "type": "boolean",
                    "description": "Return all products."
                }
            }
        }
    },
    {
        "name": "get_recommended_products",
        "description": "Get recommended product terms based on saved client info.",
        "parameters": {
            "type": "object",
            "properties": {
                "return_all": {
                    "type": "boolean",
                    "description": "Return all products."
                }
            }
        }
    },
    {
        "name": "get_available_durations",
        "description": "Get available durations for the given product.",
        "parameters": {
            "type": "object",
            "properties": {
                "get_terms": {
                    "type": "boolean",
                    "description": "Get durations."
                }
            }
        }
    },
    {
        "name": "save_loan_details",
        "description": "Save loan details for the given product.",
        "parameters": {
            "type": "object",
            "properties": {
                "program_name": {
                    "type": "string",
                    "description": "The name of the program."
                },
                "loan_amount": {
                    "type": "string",
                    "description": "The amount of the loan."
                },
                "loan_duration": {
                    "type": "string",
                    "description": "The duration of the loan."
                },
                "apy_rate": {
                    "type": "string",
                    "description": "The APY rate of the loan."
                },
                "employed_status": {
                    "type": "string",
                    "description": "The employed status of the loan."
                },
                "down_payment": {
                    "type": "string",
                    "description": "The down payment of the loan."
                },
                "annual_income": {
                    "type": "string",
                    "description": "The annual income of the loan."
                }
            }
        },
        "required": []
    },
    {
        "name": "check_missing_data",
        "description": "Check if there are missing data in the client, and try to avoid redundant requests for information already provided.",
        "parameters": {}
    }
]
