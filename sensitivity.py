from eco import TransportationScheme

SchemeA1 = TransportationScheme('voc.csv')
SchemeA2 = TransportationScheme('voc.csv', growth_rate=0.02)
schemeB = TransportationScheme('voc.csv', road_length_A = 11, \
        AADT_A=13500, AADT_A_O=3500, construction_cost_A=77000000, maintenance_cost_A=10000)
schemeB2 = TransportationScheme('voc.csv', road_length_A = 11, \
        AADT_A=13500, AADT_A_O=3500, construction_cost_A=77000000, maintenance_cost_A=10000, growth_rate = 0.02)

optimism_bias_uplifts = 1.46
constuction_cost_uplifts_A = 1.46 * 90000000
constuction_cost_uplifts_B = 1.46 * 77000000
SchemeA1.set_construction_cost(constuction_cost_uplifts_A)
SchemeA2.set_construction_cost(constuction_cost_uplifts_A)
schemeB.set_construction_cost(constuction_cost_uplifts_B)
schemeB2.set_construction_cost(constuction_cost_uplifts_B)
