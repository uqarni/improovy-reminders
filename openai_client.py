import json
from openai import OpenAI
import os

def generate_response(messages):
    openai = OpenAI()
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    for i in range(5):
        try:
            response = openai.chat.completions.create(model="gpt-4", messages=messages, max_tokens=600)
            response = json.dumps(response, default=lambda o: o.__dict__)
            response = json.loads(response)
            content = response["choices"][0]["message"]["content"]
            prompt_tokens = response['usage']['prompt_tokens']
            completion_tokens = response['usage']['completion_tokens']
            return content, prompt_tokens, completion_tokens
        except Exception as e:
            print(e)
            continue
    return False

messages = [{"role": "system", "content": "you tell one liner jokes"}]
response, p, c = generate_response(messages)


