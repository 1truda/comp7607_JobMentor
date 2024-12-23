import time
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime._exceptions import ArkAPIError

class Doubao:
    def __init__(self):
        self.client = Ark(
            api_key="3709ef67-2e62-4d03-9226-ecce7a7075a1",
            timeout=120,
            max_retries=2
        )
        self.model = "ep-20241118214429-kmtqw"

    def chat_completion(self, prompt, max_tokens=1024, stop=None, temperature=0.0, top_p=1.0, n=1):
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                stop=stop,
                temperature=temperature,
                top_p=top_p,
                n=n
            )
            return [choice.message.content for choice in completion.choices]
        except ArkAPIError as e:
            print(e)
            return None

def call_gpt(prompt, model='Doubao', stop=None, temperature=0., top_p=1.0, max_tokens=1024, majority_at=None, **kwargs):
    num_completions = majority_at if majority_at is not None else 1
    num_completions_batch_size = 5

    doubao = Doubao()
    completions = []
    
    for i in range(20 * (num_completions // num_completions_batch_size + 1)):
        try:
            requested_completions = min(num_completions_batch_size, num_completions - len(completions))
            ans = doubao.chat_completion(
                prompt=prompt,
                max_tokens=max_tokens,
                stop=stop,
                temperature=temperature,
                top_p=top_p,
                n=requested_completions,
                **kwargs
            )
            if ans:
                completions.extend(ans)
            if len(completions) >= num_completions:
                return completions[:num_completions]
        except ArkAPIError as e:
            time.sleep(min(i**2, 60))
    raise RuntimeError('Failed to call GPT API')