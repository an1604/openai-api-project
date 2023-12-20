import json
import pickle

from pydantic import BaseModel, Field
from typing import Optional

from tool_chatbot.exceptions import InvalidClientError


class ClientInfo(BaseModel):
    """Client information."""
    loan_amount: Optional[float] = Field(..., ge=0, description="Amount they wish to loan")
    duration: Optional[float] = Field(..., ge=0, description="Duration of loan (t in years).")
    down_payment_status: Optional[str] = Field(None, description="Client's down payment status (e.g., unpaid, paid)")

    @staticmethod
    def dump_client_info(client_info, dumping_type):
        if dumping_type == "dynamic":
            return
        elif dumping_type == "json":
            with open("bot_logic/client_info.json", "w") as f:
                json.dump(client_info.model_dump(), f)
        elif dumping_type == "pickle":
            with open("bot_logic/client_info.pkl", "wb") as f:
                pickle.dump(client_info, f)

    @staticmethod
    def dump_client_info_to_file(client_info):
        with open("client_info.json", "w") as f:
            json.dump(client_info, f)

    @staticmethod
    def initiate_client_info(dump=True):
        # Setup storage for Client Info
        client_info = ClientInfo(
            loan_amount=None,
            duration=None,
            down_payment=None
        )

        if dump:
            ClientInfo.dump_client_info_to_file(client_info)

        return client_info

    @staticmethod
    def assertion_client_info(client_info):
        try:
            assert client_info.loan_amount, "No loan_amount saved in client info."
            assert client_info.duration, "No duration saved in client info."
            assert client_info.down_payment_status, "No down payment status saved in client info."
            return True
        except AssertionError as e:
            raise InvalidClientError(
                f"Client information is not acceptable. Get the missing information and try again. See what is missing: {e}")

    @staticmethod
    def get_client_info(validate=True, as_object=False, dumping_type="json"):
        if dumping_type == "json":
            client_info = ClientInfo(**json.load(open("bot_logic/client_info.json", "r")))
        else:
            client_info = pickle.load(open("bot_logic/client_info.pkl", "rb"))
        if as_object:
            return client_info
        return (
            f"Loan Amount: {client_info.loan_amount}\n"
            f"Duration: {client_info.duration}\n"
            f"Down Payment: {client_info.down_payment_status}\n"
        )

    def client_info2string(self):
        return (
                'Loan Amount: ' + str(self.loan_amount) +
                '\nDuration: ' + str(self.duration) +
                '\nDown Payment: ' + str(self.down_payment_status)
        )

    def client_info_to_dict(self):
        client_info = {
            "loan_amount": self.loan_amount,
            "duration": self.duration,
            "down_payment_status": self.down_payment_status
        }
        return client_info


INFORMATION_TO_VERIFY = {
    "loan_amount": "Amount they wish to loan",
    "duration": "Duration of loan (t in years)",
    "down_payment_status": "Client's down payment status"
}
