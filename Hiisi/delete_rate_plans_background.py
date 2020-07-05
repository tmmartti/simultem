import requests
import json
import pickle
from get_token import new_token

f = open('saved_token.pckl', 'rb')
old_token = pickle.load(f)
f.close()

def delete_rps(token, ratePlanIds):
    api_url_base = 'https://api.apaleo.com/rateplan/v1/rate-plans/'

    headers = {
    'Authorization': 'Bearer {0}'.format(token)
    }
    responses = []
    for x in ratePlanIds:
        api_url = api_url_base + x
        id_specific_response = requests.delete(api_url, headers=headers)
        
    print ('Deleted!')
    
def rate_plans_to_delete(ratePlanIds):    
    try:
        delete_rps(old_token, ratePlanIds)
        print ('Used an old token')
    except:
        delete_rps(new_token, ratePlanIds)
        print ('Used a new token')