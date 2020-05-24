from FuzzyData import FuzzyWarner, create_system

fuzzy_warner = FuzzyWarner()
fuzzy_warner.create_fuzzy_functions()
fuzzy_warner.view_all_fuzzy_functions()
rules = fuzzy_warner.create_rules()

warning = create_system(rules)

warning.input['temperature'] = int(input("Temperature (C): "))
warning.input['air_humidity'] = int(input("Air humidity (%): "))
warning.input['rainless_days_period'] = int(input("Period without rain (days): "))

warning.compute()

print(warning.output['warning_level'])
fuzzy_warner.warning_level.view(sim=warning)
