from rateplan_ids import ids
from get_rate_plans import rate_plan_list, custom_list
from get_rates_and_restrictions import rate_list
from get_token import new_token
import json
import pickle
import requests

f = open('saved_token.pckl', 'rb')
old_token = pickle.load(f)
f.close()

def restrictions(rate_plan):
    try: 
        return rate_plan['restrictions']
    except: 
        return None

def pricingRule(rate_plan):
    try: 
        return rate_plan['pricingRule']
    except: 
        return None

def surcharges(rate_plan):
    try: 
        return rate_plan['surcharges']
    except: 
        return [{
        "adults": 2,
        "type": "Absolute",
        "value": 0
        },
        {
        "adults": 3,
        "type": "Absolute",
        "value": 0
        },
        {
        "adults": 4,
        "type": "Absolute",
        "value": 0
        }]

def ageCategories(rate_plan):
    try: 
        return rate_plan['ageCategories']
    except: 
        return None

def includedServices(rate_plan):
    try: 
        return rate_plan['includedServices']
    except: 
        return None

def companies(rate_plan):
    try: 
        return rate_plan['companies']
    except: 
        return None

def rp_json(rate_plan): 
    return {
        "code": str(rate_plan['code']) + 'CC',
        "propertyId": rate_plan['property']['id'],
        "unitGroupId": rate_plan['unitGroup']['id'],
        "cancellationPolicyId": rate_plan['cancellationPolicy']['id'],
        "channelCodes": rate_plan['channelCodes'],
        "serviceType": rate_plan['serviceType'],
        "vatType": rate_plan['vatType'],
        "promoCodes": None,
        "isSubjectToCityTax": rate_plan['isSubjectToCityTax'],
        "timeSliceDefinitionId": rate_plan['timeSliceDefinition']['id'],
        "name": {
            "de": 'German',
            "en": rate_plan['name']['en'].replace('-','- Pay by Card -')
        },
        "description": {
            "de": 'German',
            "en": rate_plan['description']['en'] or 'Rate'
        },
        "minGuaranteeType": 'CreditCard',
        "bookingPeriods": rate_plan['bookingPeriods'],
        "restrictions": restrictions(rate_plan),
        "pricingRule": {
            "baseRatePlanId": rate_plan['id'],
            "type": "Absolute",
            "value": 0
        },
        "surcharges": surcharges(rate_plan),
        "ageCategories": ageCategories(rate_plan),
        "includedServices": includedServices(rate_plan),
        "companies": companies(rate_plan),
        "subAccountId": rate_plan['subAccountId']
        }

def patch_json(rate_plans):
    rate_json = rate_list(rate_plans)
    return rate_json

def post_rate_plans(token, rate_plans):
    post_url = 'https://api.apaleo.com/rateplan/v1/rate-plans/'
    headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': 'Bearer {0}'.format(token)
    }
    for rate_plan in rate_plans:
        rate_plan_id = rate_plan['id']
        print (rate_plan_id)
        data = json.dumps(rp_json(rate_plan))
        requests.post(post_url, headers=headers, data=data)
        patch_url = post_url + rate_plan_id + '/rates'
        body = json.dumps(patch_json)
        requests.patch(patch_url, headers=headers, body=body)



def result(rate_plans):
    try:
        output = post_rate_plans(old_token, rate_plans)
        print ('Used an old token')
        return output
    except:
        output = post_rate_plans(new_token, rate_plans)
        print ('Used an new token')
        return output

#proplist = ['CARSNLA','CENA','HKIHAAGA','HKIPASILA','HKISORKKA','KNUMMI','LOHJA',
#'NUMMELA','RIKSU','TAMPERE1','TURKU1','VANTAA1','VANTAA2','VANTAA3']

#units = ['STDSTU','STD1BR','FAMSTU','FAM1BR','FAM2BR','STD2BR','STDROOM','STD3BR','STD4BR']


#rate_plan_list(ids(properties, unit_types, rate_plans))

rate_plan_json = rate_plan_list('all')
custom_rule = lambda elem: elem['property']['id'] in ['CENA','HKIHAAGA','HKIPASILA','HKISORKKA','KNUMMI','LOHJA',
'NUMMELA','RIKSU','TAMPERE1','VANTAA1','VANTAA2','VANTAA3']

rate_plans = custom_list(rate_plan_json,custom_rule)



