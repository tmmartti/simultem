def ids(properties, unit_types, rate_plan_codes):
    codes = []
    for prop in properties:
        for unit in unit_types:
            for rp in rate_plan_codes:
                codes.append(prop + '-' + rp + '-' + unit)
    return codes