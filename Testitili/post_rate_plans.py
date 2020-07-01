from rateplan_ids import ids
from get_rate_plans import rate_plan_list
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
        "code": str(rate_plan['code']) + 'NEW9',
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
            "en": rate_plan['name']['en'] or 'Rate'
        },
        "description": {
            "de": 'German',
            "en": rate_plan['description']['en'] or 'Rate'
        },
        "minGuaranteeType": rate_plan['minGuaranteeType'],
        "bookingPeriods": rate_plan['bookingPeriods'],
        "restrictions": restrictions(rate_plan),
        "pricingRule": pricingRule(rate_plan),
        "surcharges": surcharges(rate_plan),
        "ageCategories": ageCategories(rate_plan),
        "includedServices": includedServices(rate_plan),
        "companies": companies(rate_plan),
        "subAccountId": rate_plan['subAccountId']
        }

def post_rate_plans(token, properties, unit_types, rate_plans):
    api_url = 'https://api.apaleo.com/rateplan/v1/rate-plans/'

    headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': 'Bearer {0}'.format(token)
    }
    rp_package = rate_plan_list(ids(properties, unit_types, rate_plans))
    for rate_plan in rp_package:
        print (rate_plan['id'])
        data = json.dumps(rp_json(rate_plan))
        response = requests.post(api_url, headers=headers, data=data)
        print (json.loads(response.content))



def result(properties, unit_types, rate_plans):
    try:
        output = post_rate_plans(old_token, properties, unit_types, rate_plans)
        print ('Used an old token')
        return output
    except:
        output = post_rate_plans(new_token, properties, unit_types, rate_plans)
        print ('Used an new token')
        return output

result(['MUC'],['SGL','DBL'],['APALEO','FLEX'])