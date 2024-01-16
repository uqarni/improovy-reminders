import requests


class JustCallClient:
    def __init__(self):
        self.api_key = "a475b0ecf1d1ba78ec7a9bc49d60f225531f3617"
        self.api_secret = "bed00ba3e48de573ab7841e11971c32948edff6f"

    
    def send_text(self, them_num, us_message):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'{self.api_key}:{self.api_secret}',
        }
        data = {
            'from': "+16084205020",
            'to': them_num,
            'body': us_message
        }
        url = 'https://api.justcall.io/v1/texts/new'

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        return {"status": response_data.get("status", "unknown")}
    

