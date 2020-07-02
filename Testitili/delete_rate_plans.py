from rateplan_ids import ids
from delete_rate_plans_background import rate_plans_to_delete

def delete_rate_plans(properties, unit_types, rate_plans):
    return rate_plans_to_delete(ids(properties, unit_types, rate_plans))

rate_plans = delete_rate_plans(['MUC'],['SGL'],['APALEONEW8'])

