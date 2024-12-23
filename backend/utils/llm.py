import os
import time
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime._exceptions import ArkAPIError
from volcenginesdkarkruntime._exceptions import ArkRateLimitError


class Model:
    def __init__(self):
        pass

    def chat_completion(self, messages):
        pass


class Doubao(Model):
    def __init__(self):
        self.client = Ark(
            api_key="3709ef67-2e62-4d03-9226-ecce7a7075a1",
            timeout=120,
            max_retries=2
        )
        self.model = "ep-20241118214429-kmtqw"

    def chat_completion(self, messages):
        while True:
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                return completion.choices[0].message.content
            except ArkRateLimitError as e:
                time.sleep(3)
            except ArkAPIError as e:
                print(e)
                return None


def model_factory(model_name):
    if model_name == "Doubao":
        return Doubao()
    else:
        return Doubao()
