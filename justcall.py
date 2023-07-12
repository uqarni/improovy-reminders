import requests


def send_text(us_num, them_num, us_message, api_key, api_secret):
##SEND TEXT
    headers = {
        'Accept': 'application/json',
        'Authorization': f'{api_key}:{api_secret}',
    }
    data = {
        'from': us_num,
        'to': them_num,
        'body': us_message
    }
    url = 'https://api.justcall.io/v1/texts/new'

    response = requests.post(url, headers=headers, json=data)
    response = response.json()
    print('sendtext')
    print(response)
    return {"status": "success"}