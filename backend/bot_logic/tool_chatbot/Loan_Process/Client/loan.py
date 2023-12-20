import json

from pydantic import BaseModel, Field
from typing import Optional, Any


class Loan(BaseModel):
    program_name: Optional[str] = Field(None, description="The program name.")
    loan_amount: Optional[float] = Field(None, description="The loan amount of the program.")
    loan_duration: Optional[float] = Field(None, description="The loan duration of the program.")
    interest_rate: Optional[float] = Field(None, description="The interest rate of the program.")
    monthly_payment: Optional[float] = Field(None, description="The monthly payment of the program.")
    down_payment: Optional[float] = Field(None, description="The down payment of the program.")
    employed_status: Optional[str] = Field(None,
                                           description="The employed status of the loan (e.g., employed, self-employed)")
    apy_rate: Optional[float] = Field(None, description="The APY rate of the loan.")
    annual_income: Optional[float] = Field(None, description="The annual income of the loan.")
    created: Optional[bool] = Field(None, description="Condition for the loan creation.")

    def calculate_monthly_payment(self):
        if all([self.loan_amount is not None, self.loan_duration is not None, self.employed_status is not None]):
            monthly_payment = self.loan_amount / self.loan_duration
            self.monthly_payment = monthly_payment
            return 'The monthly payment of the loan is {}'.format(monthly_payment)
        return 'There is no monthly payment for the loan, check your spelling and try again.'

    def create_loan(self):
        if any([self.loan_amount is not None, self, self.monthly_payment is not None,
                self.down_payment is not None, self.loan_duration is not None, self.program_name is not None,
                self.employed_status is not None, self.apy_rate is not None]):
            monthly_payment = self.calculate_monthly_payment()
            if monthly_payment is not None:
                self.created = True
                return 'Loan created successfully!'.format(self.created)
        return 'Loan creation failed, check your spelling and try again'.format(self.created)

    @staticmethod
    def initiate_loan(dump):
        loan = Loan(
            program_name=None,
            employed_status=None,
            loan_duration=None,
            interest_rate=None,
            monthly_payment=None,
            down_payment=None,
            loan_amount=None,
            apy_rate=None,
            annual_income=None,
            created=False
        )
        if dump:
            Loan.dump_client_loan_to_file(loan)
        return loan

    @staticmethod
    def dump_client_loan_to_file(loan):
        with open("loan.json", "w") as f:
            json.dump(loan, f)

    def loan_to_string(self):
        return (
                'Program Name: {}'.format(self.program_name) +
                '\nEmployed Status:{}'.format(self.employed_status) +
                '\nInterest: {}'.format(self.interest_rate) +
                '\nMonthly Payment: {}'.format(self.monthly_payment) +
                '\nDown Payment: {}'.format(self.down_payment) +
                '\nLoan Amount: {}'.format(self.loan_amount) +
                '\nApy Rate: {}'.format(self.apy_rate) +
                '\nAnnual Income: {}'.format(self.annual_income) +
                '\nCreated: {}'.format(self.created)
        )
