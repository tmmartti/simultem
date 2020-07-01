from rateplan_ids import ids
from get_rate_plans import rate_plan_list
from get_token import new_token
import json
import pickle
import requests

f = open('saved_token.pckl', 'rb')
old_token = pickle.load(f)
f.close()

def rp_json(): 
    return {
    "code": "xyl",
    "propertyId": "MUC",
    "unitGroupId": "MUC-DBL",
    "cancellationPolicyId": "MUC-FLE",
    "channelCodes": [
        "Direct",
        "BookingCom",
        "Ibe"
    ],
    "serviceType": "Accommodation",
    "vatType": "Reduced",
    "promoCodes": [
        "APA55100",
        "DISCOUNT20"
    ],
    "isSubjectToCityTax": 'true',
    "timeSliceDefinitionId": "MUC-NIGHT",
    "name": {
        "de": "Nicht Stornierbar",
        "en": "Non Refundable"
    },
    "description": {
        "de": "Nicht Stornierbar",
        "en": "Non Refundable"
    },
    "minGuaranteeType": "PM6Hold",
    "bookingPeriods": [
        {
        "from": "2020-06-24T09:32:45.0891879+02:00",
        "to": "2020-07-08T09:32:45.0891879+02:00"
        },
        {
        "from": "2020-07-11T09:32:45.0891879+02:00",
        "to": "2020-08-30T09:32:45.0891879+02:00"
        }
    ],
    "restrictions": {
        "minAdvance": {
        "hours": 12,
        "days": 180
        },
        "maxAdvance": {
        "months": 24
        }
    },
    "pricingRule": {
        "baseRatePlanId": "MUC-NONREF-SGL",
        "type": "Absolute",
        "value": 20.00
    },
    "surcharges": [
        {
        "adults": 2,
        "type": "Absolute",
        "value": 10.0
        }
    ],
    "ageCategories": [
        {
        "id": "MUC-BABY",
        "surcharges": [
            {
            "adults": 1,
            "value": 20
            }
        ]
        }
    ],
    "includedServices": [
        {
        "serviceId": "MUC-BRKF",
        "grossPrice": {
            "amount": 10.0,
            "currency": "EUR"
        }
        }
    ],
  
    "subAccountId": "MUC-APALEO"
    }

def post_rate_plans(token):
    api_url = 'https://api.apaleo.com/rateplan/v1/rate-plans/'
    headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': 'Bearer {0}'.format(token)
    }
    data = json.dumps(rp_json())
    response = requests.post(api_url, headers=headers, data=data)
    if response.status_code == 200:
        print (json.loads(response.content))
    else:
        print ('Failure at posting')
        print (json.loads(response.content))


def result():
    try:
        output = post_rate_plans(old_token)
        print ('Used an old token')
        return output
    except:
        output = post_rate_plans(new_token)
        print ('Used an new token')
        return output

result()