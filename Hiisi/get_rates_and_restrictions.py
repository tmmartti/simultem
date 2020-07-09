import requests
import json
import pickle
from get_token import new_token
from get_rate_plans import rate_plan_list,custom_list

f = open('saved_token.pckl', 'rb')
old_token = pickle.load(f)
f.close()

def rate_plan_ids(custom_rule):
    rate_plan_json = rate_plan_list('all')
    custom_rate_plan_json = custom_list(rate_plan_json,custom_rule)
    id_list = []
    for rate_plan in custom_rate_plan_json:
        id_list.append(rate_plan['id'])
    return id_list

def get_rates_and_restrictions(token, ratePlanIds):
    api_url_base = 'https://api.apaleo.com/rateplan/v1/rate-plans/'

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(token)
    }
    responses = {}
    for x in ratePlanIds:
        api_url = api_url_base + x + '/rates?from=2020-08-01T17%3A00%3A00%2B02%3A00&to=2020-08-02T17%3A00%3A00%2B02%3A00'
        id_specific_response = requests.get(api_url, headers=headers)
        if id_specific_response.status_code == 200:
            append_json = json.loads(id_specific_response.content)
            responses[x] = append_json
        else:
            print ('Failed to get rate plan with id' + x)
    return responses
    
def rate_list(ratePlanIds):    
    try:
        rate_plans = get_rates_and_restrictions(old_token, ratePlanIds)
        print ('Used an old token')
        return rate_plans
    except:
        rate_plans = get_rates_and_restrictions(new_token, ratePlanIds)
        print ('Used a new token')
        return rate_plans

def restriction_list(ratePlanIds):
    try:
        rates_and_restrictions = get_rates_and_restrictions(old_token, ratePlanIds)
        restrictions = {}
        for elem in rates_and_restrictions:
            try:
                restrictions[elem] = rates_and_restrictions[elem]['rates'][0]['restrictions']
            except:
                restrictions[elem] = None
        print ('Used an old token')
        return restrictions
    except:
        rates_and_restrictions = get_rates_and_restrictions(new_token, ratePlanIds)
        restrictions = {}
        for elem in rates_and_restrictions:
            try:
                restrictions[elem] = rates_and_restrictions[elem]['rates'][0]['restrictions']
            except:
                restrictions[elem] = None
        print ('Used a new token')
        return restrictions

custom_rule = lambda elem: elem['property']['id'] not in ['CENA','HKIHAAGA','HKIPASILA','HKISORKKA','KNUMMI','LOHJA',
'NUMMELA','RIKSU','TAMPERE1','VANTAA1','VANTAA2',
'VANTAA3'] and 'promoCodes' in elem and 'PARTNER' in elem['promoCodes']

ratePlanIds = rate_plan_ids(custom_rule)

print (restriction_list(ratePlanIds))