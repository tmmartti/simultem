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
        "value": 2*EPF
        },
        {
        "adults": 4,
        "type": "Absolute",
        "value": 3*EPF
        },
        {
        "adults": 5,
        "type": "Absolute",
        "value": 4*EPF
        },
        {
        "adults": 6,
        "type": "Absolute",
        "value": 5*EPF
        },
        {
        "adults": 7,
        "type": "Absolute",
        "value": 6*EPF
        },
        {
        "adults": 8,
        "type": "Absolute",
        "value": 7*EPF
        },
        {
        "adults": 9,
        "type": "Absolute",
        "value": 8*EPF
        },
        {
        "adults": 10,
        "type": "Absolute",
        "value": 9*EPF
        },
        {
        "adults": 11,
        "type": "Absolute",
        "value": 10*EPF
        },
        {
        "adults": 12,
        "type": "Absolute",
        "value": 11*EPF
        }
    ]

def surcharge_input(n):
    d = {'code': n}
    return d

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
    if '- Pay by Invoice -' not in rate_plan['name']['en'] and '- Pay by Card -' not in rate_plan['name']['en']:
        return {
            "en": rate_plan['name']['en'].replace('-','- Pay by Invoice -'),
            "fi": rate_plan['name']['en'].replace('-','- Maksu laskulla -')
        }
    elif '- Pay by Card -' in rate_plan['name']['en']:
        return {
            "en": rate_plan['name']['en'].replace('- Pay by Card -','- Pay by Invoice -'),
            "fi": rate_plan['name']['en'].replace('- Maksu kortilla -','- Maksu laskulla -')
        }
    else:
        return {
            rate_plan['name']
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
            "fi": 'Maksu laskulla on mahdollista näin sovittaessa. 10 euron laskutuslisä (sis. ALV) lisätään laskuun. Laskutuslupa vahvistetaan ennen saapumista. \n\n Hinta sisältää 10% ALV:n, liinavaatteet, pyyhkeet, loppusiivouksen, langattoman netin, sähkön ja veden. Lisäksi sisältyy aloituspaketti, mikä sisältää muun muassa wc-paperia, käsi- ja suihkusaippuaa, shampoota, kahvia, teetä, sokeria, pippuria ja suolaa.'
        }
    else:
        return {
            "en": 'Invoicing is possible upon agreement. Invoicing fee 10 € including VAT is added to the invoices. Invoicing permit will be reviewed prior to arrival. \n\n The rate includes VAT 10%, linen, towels, final cleaning, wifi and utilities such as electricity and water. A starter pack of basic amenities such as toilet paper, hand and body soap, shampoo, coffee, tea, sugar, salt and pepper included. Every 2 weeks, a stayover cleaning will be provided.',
            "fi": 'Maksu laskulla on mahdollista näin sovittaessa. 10 euron laskutuslisä (sis. ALV) lisätään laskuun. Laskutuslupa vahvistetaan ennen saapumista. \n\n Hinta sisältää 10% ALV:n, liinavaatteet, pyyhkeet, loppusiivouksen, langattoman netin, sähkön ja veden. Lisäksi sisältyy aloituspaketti, mikä sisältää muun muassa wc-paperia, käsi- ja suihkusaippuaa, shampoota, kahvia, teetä, sokeria, pippuria ja suolaa. Hintaan sisältyy myös välisiivous joka toinen viikko.'
        }

def patch_json(new_value):
    return [
        {
            "value": new_value,
            "path": "/name",
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

def patch_trial(patch_url_base, rate_plan, headers, result_list, successful_patches, failed_patches):
    patch_url = patch_url_base[:-1]
    if patch_url != 'https://api.apaleo.com/rateplan/v1/rate-plans?ratePlanIds':
        new_value = name(rate_plan)
        patch_dict = patch_json(new_value)
        patch_data = json.dumps(patch_dict)
        print (patch_url)
        patch_response = requests.patch(patch_url, headers=headers, data=patch_data)
        print (patch_response)
        print (patch_response.content)
        if patch_response.status_code != 204:
            failed_patches += result_list
        else:
            successful_patches += result_list
        return True
    else:
        return ValueError("Pathing unsuccessful")

def patch_rate_plans(token, rate_plans, successful_patches, failed_patches):
    patch_url_base_0 = 'https://api.apaleo.com/rateplan/v1/rate-plans?ratePlanIds='
    patch_url_base_28 = 'https://api.apaleo.com/rateplan/v1/rate-plans?ratePlanIds='
    headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': 'Bearer {0}'.format(token),
    'Accept-Language': 'all'
    }
    for rate_plan in rate_plans:
        rate_plan_id = rate_plan['id']
        rate_plan = rate_plan_list([rate_plan_id])[0]
        patch_url_base_0 += rate_plan_id + ','
        try:
            patch_trial(patch_url_base_0, rate_plan, headers, [rate_plan_id], successful_patches, failed_patches)
        except:
            print ('Unsuccessful')
    print ('Number of successful patches: ' + str(len(successful_patches)))
    print ('Number of failed patches: ' + str(len(failed_patches)))



def result(rate_plans, successful_patches, failed_patches):
    try:
        output = patch_rate_plans(old_token, rate_plans, successful_patches, failed_patches)
        print ('Used an old token for post_rate_plans')
        return output
    except:
        output = patch_rate_plans(new_token, rate_plans, successful_patches, failed_patches)
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

failed = ['CENA-FLEX5APARTNER', 'CENA-FLEX5BPARTNER', 'RIKSU-FLEX5APARTNER', 'RIKSU-FLEX5BPARTNER', 'RIKSU-FLEX5CPARTNER', 'CENA-FLEX5CPARTNER', 'NUMMELA-FLEX5APARTNER', 'NUMMELA-FLEX5BPARTNER', 'NUMMELA-FLEX5CPARTNER', 'NUMMELA-FLEX5DPARTNER', 'NUMMELA-FLEX5EPARTNER']

custom_rule = lambda elem: elem['property']['id'] not in ['TURKU1', 'KNUMMI'] and 'CC' not in elem['code'] and elem['id'] not in failed and partnerCheck(elem)

rate_plans = custom_list(rate_plan_json,custom_rule)

successful_patches = []
failed_patches = []

def script_runner(interval, scale, successful_patches, failed_patches):
    for n in range(scale):
        if interval*n+interval <= len(rate_plans):
            print ('***' + str(n) + '***')
            result(rate_plans[interval*n:interval*n+interval], successful_patches, failed_patches)
        elif interval*n <= len(rate_plans) and interval*n+interval > len(rate_plans):
            print ('***' + str(n) + '***')
            result(rate_plans[interval*n:len(rate_plans)-1], successful_patches, failed_patches)
        else:
            break

script_runner(1, 160, successful_patches, failed_patches)

print (successful_patches)
print (failed_patches)
print (len(rate_plans))



