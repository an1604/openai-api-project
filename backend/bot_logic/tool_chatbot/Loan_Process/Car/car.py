import json

from pydantic import BaseModel, Field
from typing import Optional, Any

from tool_chatbot.exceptions import InvalidClientError


class Car_Details(BaseModel):
    make_and_model: Optional['str'] = Field(None,
                                            description="The make and model of the car (e.g 'Toyota Camry', 'San Francisco')")
    vin: Optional['str'] = Field(None,
                                 description="The vehicle identification number of the car (e.g '12345678901234567')")
    purchase_price: Optional['float'] = Field(None, description="The purchase price of the car (e.g '25000.0')")
    condition: Optional['str'] = Field(None, description="The condition of the car (e.g 'Used', 'New')")

    def is_missing_data(self):
        if self.make_and_model is None or self.vin is None or self.purchase_price is None or self:
            return True
        return False

    def car_to_string(self) -> str:
        return ('Make and Model: {}'.format(self.make_and_model) +
                '\nVehicle identification number(Vin): {}'.format(self.vin) +
                '\nPurchase Price: {}'.format(self.purchase_price))

    def get_car_dict(self) -> dict:
        return dict(make_and_model=self.make_and_model,
                    vin=self.vin,
                    purchase_price=self.purchase_price)

    @staticmethod
    def assert_car_details(car_details):
        try:
            assert car_details.make_and_model, 'No make and model was provided.'
            assert car_details.vin, 'No vehicle identification number was provided.'
            assert car_details.purchase_price, 'No purchase price was provided.'
            return True
        except AssertionError:
            raise InvalidClientError(
                f"Client information is not acceptable. Get the missing information and try again. See what is missing: {e}")

    @staticmethod
    def initiate_car_details(dump):
        car_details = Car_Details(
            make_and_model=None,
            purchase_price=None,
            vin=None
        )
        if dump:
            Car_Details.dump_into_file(car_details)

        return car_details

    @staticmethod
    def dump_into_file(car_details):
        with open("car_details.json", "w") as f:
            json.dump(car_details, f)