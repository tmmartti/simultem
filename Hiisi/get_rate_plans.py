import requests
import json
import pickle
from get_token import new_token

f = open('saved_token.pckl', 'rb')
old_token = pickle.load(f)
f.close()

def get_rate_plans(token, ratePlanIds):
    api_url_base = 'https://api.apaleo.com/rateplan/v1/rate-plans/'

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(token)
    }
    if ratePlanIds == 'all':
        api_url = api_url_base
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return None
    else:
        responses = []
        for x in ratePlanIds:
            api_url = api_url_base + x
            id_specific_response = requests.get(api_url, headers=headers)
            if id_specific_response.status_code == 200:
                append_json = json.loads(id_specific_response.content)
                responses.append(append_json)
            else:
                print ('Failed to get rate plan with id' + x)
        return {'ratePlans': responses}
    
def rate_plan_list(ratePlanIds):    
    try:
        rate_plans = get_rate_plans(old_token, ratePlanIds)['ratePlans']
        print ('Used an old token')
        return rate_plans
    except:
        rate_plans = get_rate_plans(new_token, ratePlanIds)['ratePlans']
        print ('Used a new token')
        return rate_plans

def custom_list(rate_plan_json, custom_rule):
    filtered_list = list(filter(custom_rule, rate_plan_json))
    return filtered_list

#rate_plan_json = rate_plan_list('all')
#custom_rule = lambda elem: elem['property']['id'] in ['CENA','HKIHAAGA','HKIPASILA','HKISORKKA','KNUMMI','LOHJA',
#'NUMMELA','RIKSU','TAMPERE1','VANTAA1','VANTAA2',
#'VANTAA3'] and 'promoCodes' in elem and 'PARTNER' in elem['promoCodes']

#print (len(custom_list(rate_plan_json,custom_rule)))