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
        "name": "open_account",
        "description": "Open account for the client if all required information has been saved.",
        "parameters": {
            "type": "object",
            "properties": {
                "open_account": {
                    "type": "boolean",
                    "description": "Open an account for the client",
                }
            },
            "required": ["open_account"],
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

    }
]
