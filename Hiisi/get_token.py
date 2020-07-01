import requests
import json
import pickle


api_url = 'https://identity.apaleo.com/connect/token'

data = {
    'grant_type': 'client_credentials'
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic WEpZSC1TUC1UT01QQU5UQUlLQVRFSERBUzpXT3ZibDJOTGJ2MjJid21HQWZZdDhBaHJNaW9FRTU='
}

def get_token():
    response = requests.post(api_url, data=data, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        print ('Fetching token failed')

new_token = get_token()['access_token']


f = open('saved_token.pckl', 'wb')
pickle.dump(new_token, f)
f.close()

