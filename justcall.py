import requests
import hashlib

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


def assign_to_group(contact_number):
    if '7372740771' in contact_number:
        return 1
    """Assigns the contact to A or B group based on their phone number"""
    # Create a new md5 hash object
    hasher = hashlib.md5()
    # Hash the phone number
    hasher.update(contact_number.encode())
    # Get the hexadecimal representation of the hash
    hash_string = hasher.hexdigest()
    # Convert the hash to an integer and return 0 for B group, 1 for A group
    return int(hash_string, 16) % 2