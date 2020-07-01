from rateplan_ids import ids
from get_rate_plans import rate_plan_list

def show_rate_plans(properties, unit_types, rate_plans):
    return rate_plan_list(ids(properties, unit_types, rate_plans))

rate_plans = show_rate_plans(['POST'],['BAS2','PRE'],['STDHIDDEN','STD','MIN1MONTH'])

if rate_plans is not None:
    print('Here are the rateplans: ')
    for rate_plan in rate_plans:
        print (str(rate_plan['id']) + ': ' + str(rate_plan['name']['en']))
else:
    print('[!] Request failed')