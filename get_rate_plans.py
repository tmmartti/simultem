import requests
import json
import pickle
from get_token import new_token

f = open('saved_token.pckl', 'rb')
old_token = pickle.load(f)
f.close()

def get_rate_plans(token):
    api_url_base = 'https://api.apaleo.com/rateplan/v1/rate-plans/'

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(token)
    }
    api_url = '{0}LND-APALEO-SGL'.format(api_url_base)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return None

try:
    rate_plans = get_rate_plans(old_token)
    print ('Used an old token')
except:
    rate_plans = get_rate_plans(new_token)
    print ('Used a new token')

if rate_plans is not None:
    print('Here are the rateplans: ')
    print(rate_plans['name'])
else:
    print('[!] Request failed') 