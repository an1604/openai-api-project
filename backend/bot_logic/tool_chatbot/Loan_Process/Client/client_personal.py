import json
import pickle
from pydantic import BaseModel, Field
from typing import Optional

from tool_chatbot.exceptions import InvalidClientError


class ClientPersonalInfo(BaseModel):
    first_name: Optional[str] = Field(None, description="first name is required")
    last_name: Optional[str] = Field(None, description="last name is required")
    annual_income: Optional[float] = Field(None, description="annual income is required")
    employment_status: Optional[str] = Field(None, description="employment status is required")
    social_security_number: Optional[str] = Field(None, description="social security number is required")

    @staticmethod
    def initiate_personal_info(dump=False):
        personal_info = ClientPersonalInfo(
            first_name=None,
            last_name=None,
            social_security_number=None,
            employment_status=None
        )
        if dump:
            ClientPersonalInfo.dump_client_info_to_file(personal_info)
        return personal_info

    @staticmethod
    def assertion_client_personal_info(client_info) -> bool:
        try:
            assert client_info.first_name, "No first name saved in client_personal_info"
            assert client_info.last_name, "No last name saved in client_personal_info."
            assert client_info.social_security_number, "No social security of the client saved in client_personal_info."
            assert client_info.annual_income, "No annual income of the client saved in client_personal_info."
            assert client_info.employment_status, "No employment status saved in client info."
            return True
        except AssertionError:
            raise InvalidClientError(
                f"Client information is not acceptable. Get the missing information and try again. See what is missing: {e}")

    @staticmethod
    def get_client_personal_info(validate=True, as_object=False, dumping_type="json"):
        if dumping_type == "json":
            client_personal_info = ClientPersonalInfo(**json.load(open("bot_logic/client_personal_info.json", "r")))
        else:
            client_personal_info = pickle.load(open("bot_logic/client_personal_info.pkl", "rb"))
        if as_object:
            return client_personal_info
        return (
            f"First name: {client_personal_info.first_name}\n"
            f"Last name: {client_personal_info.last_name}\n"
            f"Annual income: {client_personal_info.annual_income}\n"
            f"Social security number: {client_personal_info.social_security_number}\n"
            f"Employment Status: {client_personal_info.employment_status}\n"
        )

    @staticmethod
    def initiate_client_info(dump=True):
        # Setup storage for Client Info
        client_info = ClientPersonalInfo(
            first_name=None,
            last_name=None,
            annual_income=None,
            social_security_number=None,
            employment_status=None
        )

        if dump:
            ClientPersonalInfo.dump_client_info_to_file(client_info)

        return client_info

    @staticmethod
    def dump_client_info_to_file(client_info):
        with open("client_personal_info.json", "w") as f:
            json.dump(client_info, f)

    def client_personal_info_to_string(self):
        return ("First name: {}".format(self.first_name) +
                " \nLast name: {}".format(self.last_name) +
                "\nAnnual income: {}".format(self.annual_income) +
                "\nSocial security number: {}".format(self.social_security_number) +
                "\nEmployment Status: {}".format(self.employment_status))
