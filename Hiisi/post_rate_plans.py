from rateplan_ids import ids
from get_rate_plans import rate_plan_list
import json
import pickle
import requests

f = open('saved_token.pckl', 'rb')
old_token = pickle.load(f)
f.close()

def rp_json(rate_plan): 
    return {
        "code": rate_plan.code + 'NEW',
        "propertyId": rate_plan.property.id,
        "unitGroupId": rate_plan.unitGroup.id,
        "cancellationPolicyId": rate_plan.cancellationPolicy.id,
        "channelCodes": rate_plan.channelCodes,
        "serviceType": rate_plan.serviceType,
        "vatType": rate_plan.vatType,
        "promoCodes": rate_plan.promoCodes or 'X',
        "isSubjectToCityTax": rate_plan.isSubjectToCityTax,
        "timeSliceDefinitionId": rate_plan.timeSliceDefinition.id,
        "name": {
            "de": rate_plan.name.de or 'Pris',
            "en": rate_plan.name.en or 'Rate'
        },
        "description": {
            "de": rate_plan.description.de or 'Pris',
            "en": rate_plan.description.en or 'Rate'
        },
        "minGuaranteeType": rate_plan.minGuaranteeType,
        "bookingPeriods": rate_plan.bookingPeriods,
        "restrictions": rate_plan.restrictions,
        "pricingRule": rate_plan.pricingRule,
        "surcharges": rate_plan.surcharges,
        "ageCategories": rate_plan.ageCategories,
        "includedServices": rate_plan.includedServices,
        "companies": rate_plan.companies,
        "subAccountId": rate_plan.subAccount.id
        }

def post_rate_plans(token, properties, unit_types, rate_plans):
    api_url = 'https://api.apaleo.com/rateplan/v1/rate-plans/'

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(token)
    }
    for rate_plan in rate_plan_list(ids(properties, unit_types, rate_plans)):
        body = rp_json(rate_plan)
        response = requests.post(api_url, headers=headers, body=body)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return None