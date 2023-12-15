import logging
import os
from dotenv import load_dotenv

load_dotenv('.env')


def get_log_name(logs_path: str = "logs", fn_prefix: str = "chatbot", fn_suffix: str = "log") -> str:
    log_files = [x for x in os.listdir(logs_path) if f".{fn_suffix}" in x]
    if log_files:
        uuid = max([int(x.split(".")[0].split("_")[-1])
                   for x in log_files]) + 1
    else:
        uuid = 1
    return f"{fn_prefix}_{uuid}.{fn_suffix}"


def setup_logger():
    LOG_TO_FILE_ENABLED = bool(int(os.getenv('LOG_TO_FILE_ENABLED')))
    LOGS_PATH = os.getenv('LOGS_PATH')

    if LOG_TO_FILE_ENABLED:
        print("Logging to file enabled")
        
        logging.basicConfig(
            filename=f"{LOGS_PATH}/{get_log_name(LOGS_PATH)}", level=logging.INFO, filemode="w"
        )
    else:
        print("Logging to file disabled")
        logging.basicConfig(level=logging.INFO)
