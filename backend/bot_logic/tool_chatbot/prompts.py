import os

from tool_chatbot.helper_functions import get_text_from_file

END_OF_PROMPT_EDITION = """
Did you understand my request clearly?
"""


ROLE = get_text_from_file('/mnt/c/Users/adina/Desktop/תקיית_עבודות/chatbot-shira-fe-fixes/backend/bot_logic/prompts/role.txt')

GENERAL_CONVERSATION = get_text_from_file('/mnt/c/Users/adina/Desktop/תקיית_עבודות/chatbot-shira-fe-fixes/backend/bot_logic/prompts/GeneralConversationGuidelines.txt')

CREATE_LOAN_PROMPT = """
You create a car loan and no more steps and information are needed. 
The client does not need to call or go to the bank. 
If there is any issue, suggest connecting to the human representative (use request_human_rep function).
"""

CLIENT_INFO_PROMPT = """
Don't ask for customer details that you already have collected in the conversation.
You don't need more details than the Client Details to open an account.
IF YOU ASK FOR UNNECESSARY PERSONAL INFORMATION, YOU MIGHT RISK THE CUSTOMER'S PRIVACY AND CAUSE FINANCIAL DAMAGES.
"""

REMEMBER_PROMPT = {
    'role': 'system',
    'content': get_text_from_file('bot_logic/prompts/remember.txt')
}

ROLE_TEMPLATE = 'Role: {}\n{}'
CONTEX_TEMPLATE = '\nContex: {}\n'
PROMPT_TEMPLATE = '{}\n{}{}{}'
CREATE_LOAN_TEMPLATE = 'Create loan: {}'
