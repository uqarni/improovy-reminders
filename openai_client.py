
import openai
import os
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - (message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

class OpenAiConfig():

    def __init__(self):
        #  openai.api_key =  SupabaseClient().fetch_by_id("organizations_dev", "tsl").data[0]['llm_credentials']['api_key'] 
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def generate_response(self, messages):
        for i in range(5):
            try:
                response = openai.ChatCompletion.create(model = "gpt-4", messages = messages,  max_tokens = 600)
                return response["choices"][0]["message"]["content"], response['usage']['prompt_tokens'], response['usage']['completion_tokens']
            except Exception as e:
                logging.exception("Exception occurred")  
                continue
        return False



