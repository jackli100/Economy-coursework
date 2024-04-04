from eco import TransportationScheme

SchemeA1 = TransportationScheme('voc.csv')
SchemeA2 = TransportationScheme('voc.csv', growth_rate=0.02)
schemeB1 = TransportationScheme('voc.csv', road_length_A = 11, \
        AADT_A=13500, AADT_A_O=3500, construction_cost_A=77000000, maintenance_cost_A=10000)
schemeB2 = TransportationScheme('voc.csv', road_length_A = 11, \
        AADT_A=13500, AADT_A_O=3500, construction_cost_A=77000000, maintenance_cost_A=10000, growth_rate = 0.02)
resultA1 = SchemeA1.financial_metrics
resultA2 = SchemeA2.financial_metrics
resultB1 = schemeB1.financial_metrics
resultB2 = schemeB2.financial_metrics
print(f"SchemeA1: {resultA1}")
print(f"SchemeA2: {resultA2}")
print(f"SchemeB1: {resultB1}")
print(f"SchemeB2: {resultB2}")