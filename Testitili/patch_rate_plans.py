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

def min_stay_json(restriction_dict, rate_plan_id):
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

def description(minStay):
    if minStay[0]['value']['minLengthOfStay'] != 28:
        return {
            "en": 'Invoicing is possible upon agreement. Invoicing fee 10 € including VAT is added to the invoices. Invoicing permit will be reviewed prior to arrival. \n\n The rate includes VAT 10%, linen, towels, final cleaning, wifi and utilities such as electricity and water. A starter pack of basic amenities such as toilet paper, hand and body soap, shampoo, coffee, tea, sugar, salt and pepper included.',
            "de": 'Maksu laskulla on mahdollista näin sovittaessa. 10 euron laskutuslisä (sis. ALV) lisätään laskuun. Laskutuslupa vahvistetaan ennen saapumista. \n\n Hinta sisältää 10% ALV:n, liinavaatteet, pyyhkeet, loppusiivouksen, langattoman netin, sähkön ja veden. Lisäksi sisältyy aloituspaketti, mikä sisältää muun muassa wc-paperia, käsi- ja suihkusaippuaa, shampoota, kahvia, teetä, sokeria, pippuria ja suolaa.'
        }
    else:
        return {
            "en": 'Invoicing is possible upon agreement. Invoicing fee 10 € including VAT is added to the invoices. Invoicing permit will be reviewed prior to arrival. \n\n The rate includes VAT 10%, linen, towels, final cleaning, wifi and utilities such as electricity and water. A starter pack of basic amenities such as toilet paper, hand and body soap, shampoo, coffee, tea, sugar, salt and pepper included. Every 2 weeks, a stayover cleaning will be provided.',
            "de": 'Maksu laskulla on mahdollista näin sovittaessa. 10 euron laskutuslisä (sis. ALV) lisätään laskuun. Laskutuslupa vahvistetaan ennen saapumista. \n\n Hinta sisältää 10% ALV:n, liinavaatteet, pyyhkeet, loppusiivouksen, langattoman netin, sähkön ja veden. Lisäksi sisältyy aloituspaketti, mikä sisältää muun muassa wc-paperia, käsi- ja suihkusaippuaa, shampoota, kahvia, teetä, sokeria, pippuria ja suolaa. Hintaan sisältyy myös välisiivous joka toinen viikko.'
        }

def patch_json(new_value):
    return [
        {
            "value": new_value,
            "path": "/description",
            "op": "replace"
        }
    ]

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
            

def rp_json(rate_plan, patch_json): 
    return {
        "code": str(rate_plan['code']),
        "propertyId": rate_plan['property']['id'],
        "unitGroupId": rate_plan['unitGroup']['id'],
        "cancellationPolicyId": rate_plan['cancellationPolicy']['id'],
        "channelCodes": rate_plan['channelCodes'],
        "serviceType": 'Accommodation',
        "vatType": vatType(rate_plan),
        "promoCodes": promoCodes(rate_plan),
        "isSubjectToCityTax": rate_plan['isSubjectToCityTax'],
        "timeSliceDefinitionId": rate_plan['timeSliceDefinition']['id'],
        "name": name(rate_plan),
        "description": description(patch_json),
        "minGuaranteeType": 'CreditCard',
        "bookingPeriods": bookingPeriods(rate_plan),
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
        "subAccountId": subAccountId(rate_plan)
        }

def restriction_json(rate_plans):
    rate_json = restriction_list(rate_plans)
    return rate_json

def patch_rate_plans(token, rate_plans):
    patch_url_base_1 = 'https://api.apaleo.com/rateplan/v1/rate-plans?ratePlanIds='
    patch_url_base_2 = 'https://api.apaleo.com/rateplan/v1/rate-plans?ratePlanIds='
    headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': 'Bearer {0}'.format(token),
    'Accept-Language': 'all'
    }
    ratePlanIds = []
    successful_patches = []
    failed_patches = []
    under28 = []
    over28 = []
    for rate_plan in rate_plans:
        ratePlanIds.append(rate_plan['id'])
    restriction_dict = restriction_json(ratePlanIds)
    for rate_plan_id in ratePlanIds:
        minStay = min_stay_json(restriction_dict, rate_plan_id)
        if minStay[0]['value']['minLengthOfStay'] != 28:
            patch_url_base_1 += rate_plan_id + ','
            minStay_1 = minStay
            under28.append(rate_plan_id)
        else:
            patch_url_base_2 += rate_plan_id + ','
            minStay_2 = minStay
            over28.append(rate_plan_id)
    patch_url_1 = patch_url_base_1[:-1] + '&from=2020-07-23&to=2024-08-03'
    patch_url_2 = patch_url_base_2[:-1] + '&from=2020-07-23&to=2024-08-03'
    new_value_1 = description(minStay_1)
    new_value_2 = description(minStay_2)
    patch_dict_1 = patch_json(new_value_1)
    patch_dict_2 = patch_json(new_value_2)
    patch_data_1 = json.dumps(patch_dict_1)
    patch_data_2 = json.dumps(patch_dict_2)
    print (patch_url_1)
    print (patch_url_2)
    print (patch_data_1)
    if patch_url_1 != 'https://api.apaleo.com/rateplan/v1/rate-plans?ratePlanIds=':
        patch_response_1 = requests.patch(patch_url_1, headers=headers, data=patch_data_1)
        print (patch_response_1)
        print (patch_response_1.content)
        if patch_response_1.status_code != 204:
            failed_patches.append(rate_plan_id)
        else:
            successful_patches = ratePlanIds
    if patch_url_2 != 'https://api.apaleo.com/rateplan/v1/rate-plans?ratePlanIds=':
        patch_response_2 = requests.patch(patch_url_2, headers=headers, data=patch_data_2)
        print (patch_response_2)
        print (patch_response_2.content)
        if patch_response_2.status_code != 204:
            failed_patches.append(rate_plan_id)
        else:
            successful_patches = ratePlanIds
    
    print (successful_patches)
    print (failed_patches)



def result(rate_plans):
    try:
        output = patch_rate_plans(old_token, rate_plans)
        print ('Used an old token for post_rate_plans')
        return output
    except:
        output = patch_rate_plans(new_token, rate_plans)
        print ('Used an new token')
        return output

#proplist = ['CARSNLA','CENA','HKIHAAGA','HKIPASILA','HKISORKKA','KNUMMI','LOHJA',
#'NUMMELA','RIKSU','TAMPERE1','TURKU1','VANTAA1','VANTAA2','VANTAA3']

#units = ['STDSTU','STD1BR','FAMSTU','FAM1BR','FAM2BR','STD2BR','STDROOM','STD3BR','STD4BR']


#rate_plan_list(ids(properties, unit_types, rate_plans))

rate_plan_json = rate_plan_list('all')['ratePlans']

def partnerCheck(elem):
    if 'promoCodes' in elem:
        if 'PARTNER' in elem['promoCodes']:
            return True
    else:
        return False

custom_rule = lambda elem: elem['property']['id'] in ['BER'] #and partnerCheck(elem)

rate_plans = custom_list(rate_plan_json,custom_rule)


result(rate_plans)



