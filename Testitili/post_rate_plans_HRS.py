from rateplan_ids import ids
from get_rate_plans import rate_plan_list, custom_list
from get_unit_groups import unit_group_list
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
    if '5' in rate_plan['code']:
        EPF = 5
    elif '6' in rate_plan['code']:
        EPF = 3
    else:
        EPF = 10
    return [
        {
        "adults": 2,
        "type": "Absolute",
        "value": EPF
        },
        {
        "adults": 3,
        "type": "Absolute",
        "value": EPF
        },
        {
        "adults": 4,
        "type": "Absolute",
        "value": EPF
        },
        {
        "adults": 5,
        "type": "Absolute",
        "value": EPF
        },
        {
        "adults": 6,
        "type": "Absolute",
        "value": EPF
        },
        {
        "adults": 7,
        "type": "Absolute",
        "value": EPF
        },
        {
        "adults": 8,
        "type": "Absolute",
        "value": EPF
        },
        {
        "adults": 9,
        "type": "Absolute",
        "value": EPF
        }
    ]

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

def serviceType(rate_plan):
    try: 
        return rate_plan['serviceType']
    except: 
        return None

def vatType(rate_plan):
    try: 
        return rate_plan['vatType']
    except: 
        return None

def promoCodes(rate_plan):
    try: 
        return rate_plan['promoCodes']
    except: 
        return None

def name(rate_plan):
    try: 
        return {
            "en": rate_plan['name']['en'].replace('-','- Pay by Card -'),
            "fi": rate_plan['name']['en'].replace('-','- Maksu kortilla -')
        }
    except:
        return {
            "en": rate_plan['name']['en'].replace('-','- Pay by Card -')
        }

def patch_json(restriction_dict, rate_plan_id):
    try: 
        minStay = restriction_dict[rate_plan_id]['minLengthOfStay']
    except:
        minStay = None
    try: 
        maxStay = restriction_dict[rate_plan_id]['maxLengthOfStay']
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

def description(patch_json):
    if patch_json['value']['minLengthOfStay'] != 28:
        return {
            "en": 'Payment will be charged from the card provided prior to arrival. The rate includes VAT 10%, linen, towels, final cleaning, wifi and utilities such as electricity and water. A starter pack of basic amenities such as toilet paper, hand and body soap, shampoo, coffee, tea, sugar, salt and pepper included.',
            "fi": 'Maksu veloitetaan kortilta ennen saapumista. Hinta sisältää 10% ALV:n, liinavaatteet, pyyhkeet, loppusiivouksen, langattoman netin, sähkön ja veden. Lisäksi sisältyy aloituspaketti, mikä sisältää muun muassa wc-paperia, käsi- ja suihkusaippuaa, shampoota, kahvia, teetä, sokeria, pippuria ja suolaa.'
        }
    else:
        return {
            "en": 'Payment will be charged from the card provided prior to arrival. The rate includes VAT 10%, linen, towels, final cleaning, wifi and utilities such as electricity and water. A starter pack of basic amenities such as toilet paper, hand and body soap, shampoo, coffee, tea, sugar, salt and pepper included. Every 2 weeks, a stayover cleaning will be provided.',
            "fi": 'Maksu veloitetaan kortilta ennen saapumista. Hinta sisältää 10% ALV:n, liinavaatteet, pyyhkeet, loppusiivouksen, langattoman netin, sähkön ja veden. Lisäksi sisältyy aloituspaketti, mikä sisältää muun muassa wc-paperia, käsi- ja suihkusaippuaa, shampoota, kahvia, teetä, sokeria, pippuria ja suolaa. Hintaan sisältyy myös välisiivous joka toinen viikko.'
        }

def bookingPeriods(rate_plan):
    try:
        return rate_plan['bookingPeriods']
    except:
        return None

def subAccountId(rate_plan):
    try:
        return rate_plan['subAccountId']
    except:
        return None

def includedServices(rate_plan):
    try :
        result = []
        for incl_serv in rate_plan['includedServices']:
            service = {
            "serviceId": incl_serv['serviceId'],
            "grossPrice": incl_serv['grossPrice']
            }
            result.append(service)
        return result
    except:
        return None
            

def rp_json(rate_plan, property_id, unit_group, master_rate): 
    return {
        "code": 'NONREFAHRS',
        "propertyId": property_id,
        "unitGroupId": unit_group['id'],
        "cancellationPolicyId": master_rate['cancellationPolicy']['id'],
        "channelCodes": rate_plan['channelCodes'],
        "serviceType": 'Accommodation',
        "vatType": vatType(rate_plan),
        "promoCodes": promoCodes(rate_plan),
        "isSubjectToCityTax": rate_plan['isSubjectToCityTax'],
        "timeSliceDefinitionId": master_rate['timeSliceDefinition']['id'],
        "name": rate_plan['name'],
        "description": rate_plan['description'],
        "minGuaranteeType": rate_plan['minGuaranteeType'],
        "bookingPeriods": bookingPeriods(rate_plan),
        "restrictions": restrictions(rate_plan),
        "pricingRule": {
            "baseRatePlanId": master_rate['id'],
            "type": "Absolute",
            "value": 0
        },
        "surcharges": surcharges(rate_plan),
        "ageCategories": ageCategories(rate_plan),
        "includedServices": includedServices(rate_plan),
        "companies": companies(rate_plan),
        "subAccountId": subAccountId(master_rate)
        }

def restriction_json(rate_plans):
    rate_json = restriction_list(rate_plans)
    return rate_json

def post_rate_plans(token, rate_plans, properties):
    post_url = 'https://api.apaleo.com/rateplan/v1/rate-plans/'
    patch_url_base = 'https://api.apaleo.com/rateplan/v1/rates?ratePlanIds='
    patch_url_end = ',&from=2020-07-21T17%3A00%3A00%2B02%3A00&to=2024-08-03T17%3A00%3A00%2B02%3A00'
    headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': 'Bearer {0}'.format(token),
    'Accept-Language': 'all'
    }
    ratePlanIds = []
    failed_posts = []
    successful_posts = []
    failed_patches = []
    for rate_plan in rate_plans:
        ratePlanIds.append(rate_plan['id'])
    restriction_dict = restriction_json(ratePlanIds)
    master_rates = {
        'CENA': 'CENA-NONREF2A',
        'VANTAA3': 'VANTAA3-NONREF2A-STDSTU',
        'TURKU1': 'TURKU1-NONREF2A',
        'HKIHAAGA': 'HKIHAAGA-NONREF2A'
    }
    for rate_plan_id in ratePlanIds:
        rate_plan = rate_plan_list([rate_plan_id])[0]
        rate_plan_code = rate_plan['code']
        patch_dict = patch_json(restriction_dict,rate_plan_id)
        for property_id in properties:
            unit_groups = unit_group_list([property_id])[0]['unitGroups']
            master_rate_id = master_rates[property_id]
            master_rate = rate_plan_list([master_rate_id])[0]
            for unit_group in unit_groups:
                unit_type = unit_group['code']
                new_rp_id = property_id + '-' + 'NONREFAHRS' + '-' + unit_type
                print (new_rp_id)
                data = json.dumps(rp_json(rate_plan, property_id, unit_group, master_rate))
                post_response = requests.post(post_url, headers=headers, data=data)
                print (post_response)
                if post_response.status_code != 201:
                    failed_posts.append(new_rp_id)
                    print (post_response.content)
                else:
                    successful_posts.append(new_rp_id)
                patch_url = patch_url_base + new_rp_id + patch_url_end
                patch_data = json.dumps(patch_dict)
                print (patch_url)
                print (patch_data)
                patch_response = requests.patch(patch_url, headers=headers, data=patch_data)
                print (patch_response)
                if patch_response.status_code != 204:
                    failed_patches.append(new_rp_id)
    print (successful_posts)
    print (failed_posts)
    print (failed_patches)



def result(rate_plans, properties):
    try:
        output = post_rate_plans(old_token, rate_plans, properties)
        print ('Used an old token for post_rate_plans')
        return output
    except:
        output = post_rate_plans(new_token, rate_plans, properties)
        print ('Used an new token')
        return output

#proplist = ['CARSNLA','CENA','HKIHAAGA','HKIPASILA','HKISORKKA','KNUMMI','LOHJA',
#'NUMMELA','RIKSU','TAMPERE1','TURKU1','VANTAA1','VANTAA2','VANTAA3']

#units = ['STDSTU','STD1BR','FAMSTU','FAM1BR','FAM2BR','STD2BR','STDROOM','STD3BR','STD4BR']

rate_plan_json = rate_plan_list('all')['ratePlans']

custom_rule = lambda elem: elem['code'] in ['NONREFAHRS'] and elem['property']['id'] in ['CENA', 'HKIHAAGA', 'TURKU1', 'VANTAA3']

rate_plans = custom_list(rate_plan_json,custom_rule)


result(rate_plans, ['CENA'])



