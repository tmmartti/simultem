from rateplan_ids import ids
from get_rate_plans import rate_plan_list, custom_list
from get_rates_and_restrictions import restriction_list
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

def restriction_json(rate_plans):
    rate_json = restriction_list(rate_plans)
    return rate_json

def patch_json(restriction_dict, rate_plan):
    try: 
        minStay = restriction_dict[rate_plan]['minLengthOfStay']
    except:
        minStay = None
    try: 
        maxStay = restriction_dict[rate_plan]['maxLengthOfStay']
    except:
        maxStay = None
    return [
        {
            "value": {
                        "minLengthOfStay": minStay,
                        "maxLengthOfStay": maxStay,
                        "closed": False,
                        "closedOnArrival": False,
                        "closedOnDeparture": False
                        },
            "path": "/restrictions",
            "op": "add"
        }
    ]

def post_rate_plans(token, rate_plans):
    post_url = 'https://api.apaleo.com/rateplan/v1/rate-plans/'
    patch_url_base = 'https://api.apaleo.com/rateplan/v1/rates?ratePlanIds='
    patch_url_end = ',&from=2020-07-10T17%3A00%3A00%2B02%3A00&to=2024-08-03T17%3A00%3A00%2B02%3A00'
    headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': 'Bearer {0}'.format(token)
    }
    restriction_dict = restriction_json(rate_plans)
    for rate_plan in rate_plans:
        rate_plan_id = rate_plan['id']
        print (rate_plan_id)
        data = json.dumps(rp_json(rate_plan))
        requests.post(post_url, headers=headers, data=data)
        patch_url = patch_url_base + rate_plan_id + patch_url_end
        body = json.dumps(patch_json(restriction_dict,rate_plan))
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



