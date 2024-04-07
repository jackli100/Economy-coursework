from eco import TransportationScheme

SchemeA1 = TransportationScheme('voc.csv')
SchemeA2 = TransportationScheme('voc.csv', growth_rate=0.02)
schemeB1 = TransportationScheme('voc.csv', road_length_A = 11, \
        AADT_A=13500, AADT_A_O=3500, construction_cost_A=77000000, maintenance_cost_A=10000)
schemeB2 = TransportationScheme('voc.csv', road_length_A = 11, \
        AADT_A=13500, AADT_A_O=3500, construction_cost_A=77000000, maintenance_cost_A=10000, growth_rate = 0.02)
SchemeA1.get_things_done()
SchemeA2.get_things_done()
schemeB1.get_things_done()
schemeB2.get_things_done()
schemeB1.save_data_to_csv('schemeB1.csv')