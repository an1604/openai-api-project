import json
import pickle

from pydantic import BaseModel, Field
from typing import Optional
from ..Car.car import Car_Details
from .loan import Loan
from .clientInfo import ClientInfo
from .client_personal import ClientPersonalInfo
from ...exceptions import InvalidClientError


class Client(BaseModel):
    client_info: Optional[ClientInfo] = Field(None, description="The financial client information.")
    client_personal_info: Optional[ClientPersonalInfo] = Field(None, description="The personal information.")
    car_details: Optional[Car_Details] = Field(None, description="The car details.")
    loan: Optional[Loan] = Field(None, description="The that suitable for the client.")




    def get_car_details(self) -> Car_Details:
        return self.car_details

    def get_client_info(self) -> ClientInfo:
        return self.client_info

    def get_client_personal_info(self) -> ClientPersonalInfo:
        return self.client_personal_info

    def get_loan(self) -> Loan:
        return self.loan


    def client_to_string(self) -> str:
        return ("Client personal information: {}\n".format(self.client_personal_info.client_personal_info_to_string())
                + "Client info: {}\n".format(self.client_info.client_info2string()) +
                "\nCar Details: {}".format(self.car_details.car_to_string()) +
                "\nLoan: {}".format(self.loan.loan_to_string()))

    @staticmethod
    def initiate_client(dump=False):
        client_info = ClientInfo.initiate_client_info(dump)
        client_personal_info = ClientPersonalInfo.initiate_personal_info(dump)
        car_details = Car_Details.initiate_car_details(dump)
        loan = Loan.initiate_loan(dump)

        client = Client(client_info=client_info, client_personal_info=client_personal_info, car_details=car_details,
                        loan=loan)

        if dump:
            Client.dump_client_to_file(client)
        return client

    @staticmethod
    def dump_client(client, dumping_type):
        if dumping_type == "dynamic":
            return
        elif dumping_type == "json":
            with open("bot_logic/client.json", "w") as f:
                json.dump(client.model_dump(), f)
        elif dumping_type == "pickle":
            with open("bot_logic/client.pkl", "wb") as f:
                pickle.dump(client, f)

    @staticmethod
    def dump_client_to_file(client):
        with open("client.json", "w") as f:
            json.dump(client, f)

    @staticmethod
    def load_client_from_file(client_file):
        with open("client.json", "r") as f:
            return pickle.load(f)

    @staticmethod
    def assertion_is_valid(client):
        try:
            ClientInfo.assertion_client_info(client.get_client_info())
            ClientPersonalInfo.assertion_client_personal_info(client.get_client_personal_info())
            Car_Details.assert_car_details(client.get_car_details())
            return True
        except AssertionError as e:
            raise InvalidClientError(
                f"Client information is not acceptable. Get the missing information and try again. See what is missing: {e}")

    @staticmethod
    def get_client(validate=True, as_object=False, dumping_type="json"):
        if dumping_type == "json":
            client = Client(**json.load(open("bot_logic/client.json", "r")))
        else:
            client = pickle.load(open("bot_logic/client.pkl", "rb"))
        if as_object:
            return client
        return (
                "Client personal information: {}".format(
                    client.get_client_personal_info().client_personal_info_to_string()) +
                "\nClient financial information: {}".format(client.get_client_info().client_info2string()) +
                "\nCar Details: {}".format(client.get_car_details().car_to_string()) +
                "\nLoan: {}".format(client.get_loan().loan_to_string())
        )
