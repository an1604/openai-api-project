import time

import openai
from openai.error import RateLimitError


class ModerationModel:
    def __init__(self):
        self.moderation_model = openai.Moderation()
        self.moderation_model_name = "text-moderation-latest"

    def predict_violating_content(self, user_input):
        # TODO: COMMENT THIS FUNCTION FOR SAVING API REQUESTS
        # stop = False
        # while not stop:
        #     try:
        #         response = self.moderation_model.create(
        #             input=user_input,
        #             model=self.moderation_model_name
        #         )
        #         stop = True
        #     except RateLimitError as e:
        #         time.sleep(20)
        #         stop = False
        # return response['results'][0]['flagged']
        return False
