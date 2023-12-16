functions = [
    {
        "name": "save_client_info",
        "description": "Save client info. This needs to be called always when the client provides new information or when he updates his information. ",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "Amount they wish to deposit (P).",
                },
                "duration": {
                    "type": "number",
                    "description": "Duration of deposit in years. Use float for months or weeks (e.g. 0.5 for 6 months).",
                },
                "withdrawal_preference": {
                    "type": "string",
                    "enum": ["end_of_term", "monthly"],
                    "description": "Withdrawal preference (end of the term or every month).",
                },
            },
            "required": [],
        },
    },
    {
        "name": "query_knowledgebase",
        "description": "Query the knowledgebase to answer a general question about the products. The question should be formulated in a way that no further context is required to answer it.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Question to ask the knowledgebase.",
                }
            },
            "required": ["question"],
        },
    },
    {
        "name": "calculate_interest",
        "description": "Calculate total amount after interest based on a recommended program.",
        "parameters": {
            "type": "object",
            "properties": {
                "principal": {
                    "type": "number",
                    "description": "Principal amount (P).",
                },
                "program": {
                    "type": "string",
                    "description": "Name of recommended program.",
                },
            },
            "required": ["principal", "program"],
        },
    },
    {
        "name": "request_human_rep",
        "description": "Request human representative",
        "parameters": {
            "type": "object",
            "properties": {
                "request_human_rep": {
                    "type": "boolean",
                    "description": "Request human representative",
                }
            },
        },
    },
    {
        "name": "get_product_terms",
        "description": "Call this function to retrieve product details.",
        "parameters": {
            "type": "object",
            "properties": {
                "return_all": {
                    "type": "boolean",
                    "description": "Return all products.",
                }
            },
        },
    },
    {
        "name": "get_recommended_products",
        "description": "Get recommended product terms based on saved client info",
        "parameters": {
            "type": "object",
            "properties": {
                "return_all": {
                    "type": "boolean",
                    "description": "Return all products.",
                }
            },
        },
    },
    {
        "name": "get_available_durations",
        "description": "Get available durations for the given product.",
        "parameters": {
            "type": "object",
            "properties": {
                "get_terms": {
                    "type": "boolean",
                    "description": "Get durations",
                }
            },
        },

    },
    {
        'name': 'crate_loan',
        'description': 'Creating the loan after checking  the dependencies attributes from the client_info dictionary.',
        'parameters': {
            'client_info': {
                'type': 'object',
                'description': 'A dictionary containing the client information.',
                'properties': {
                    'amount': {
                        'type': 'float',
                        'description': 'Amount they wish to loan'
                    },
                    'duration': {
                        'type': 'float',
                        'description': '{Duration of the loan(t in years).'
                    },
                    'credit_score': {
                        'type': 'int',
                        'description': "Client's credit score. A higher credit score can lead to better loan terms."
                    },
                    'monthly_income': {
                        'type': 'float',
                        'description': "Client's monthly income. Lenders often consider income when approving loans."
                    },
                    'employment_status': {
                        'type': 'string',
                        'description': "Client's employment status (e.g., employed, self-employed, unemployed)."
                    },
                    'existing_debt': {
                        'type': 'string',
                        'description': "Total amount of existing debt (e.g., other loans, credit card balances)."
                    },
                    'down_payment': {
                        'type': 'float',
                        'description': "The down payment made by the client, if any."
                    }
                },

            }
        },
        'returns': {
            'type': 'string',
            'description': 'A message indicating the success or failure of the loan creation process.'
        }
    }
]
