from eco import TransportationScheme

class EcoPetrol(TransportationScheme):

    def __init__(self, csv_file_path = 'voc.csv', transport_scheme_name = 'A_low', value_of_time = 10.79, road_length_O=5, average_speed_O=22, AADT_O=15000,
                 road_length_A=9, average_speed_A=65, average_speed_A_O=28, AADT_A=13000,
                 AADT_A_O=4000, construction_cost_A=90000000, maintenance_cost_A=10000, growth_rate = 0.01, VAT = 0.2, project_life = 60,
                 discount_rate_1 = 0.035, discount_rate_2 = 0.03, petorl_kg_per_litre = 2.11):
        self.transport_scheme_name = transport_scheme_name
        # 设置scheme O变量
        self.road_length_O = road_length_O
        self.average_speed_O = average_speed_O
        self.AADT_O = AADT_O
        
        # 设置scheme A变量
        self.road_length_A = road_length_A
        self.average_speed_A = average_speed_A
        self.average_speed_A_O = average_speed_A_O
        self.AADT_A = AADT_A
        self.AADT_A_O = AADT_A_O
        self.construction_cost_A = construction_cost_A
        self.maintenance_cost_A = maintenance_cost_A
        self.growth_rate = growth_rate
        self.value_of_time_initial = value_of_time
        self.the_value_of_time_2030 = self.value_of_time_initial * 1.5893 * 125.57 / 104.88
        self.vat = 0.2
        self.project_life = project_life
        self.end_year = 2030 + self.project_life
        self.discount_rate_1 = discount_rate_1
        self.discount_rate_2 = discount_rate_2
        self.tf = 0.2
        self.petorl_kg_per_litre = petorl_kg_per_litre

        # 加载CSV文件数据
        self.data_dict = self.load_csv_data(csv_file_path)

        # 计算未来AADT的值
        self.future_AADT_A = self.get_future_AADT(self.AADT_A, self.growth_rate, 2031, 2090, 20)
        self.future_AADT_A_O = self.get_future_AADT(self.AADT_A_O, self.growth_rate, 2031, 2090, 20)
        self.future_AADT_O = self.get_future_AADT(self.AADT_O, self.growth_rate, 2031, 2090, 20, is_special_case=True)

        # 计算未来价值的时间
        self.value_of_time_dict = self.get_value_of_time(2031, 2091, self.the_value_of_time_2030, self.long_term_growth_rate)
        
        # 大字典存储所有的成本和收益
        self.costs_benefits = {
        'GC_work_fuel_cost_A': {},
        'GC_work_fuel_cost_A_O': {},
        'GC_work_fuel_cost_O': {},
        'GC_non_work_fuel_cost_A': {},
        'GC_non_work_fuel_cost_A_O': {},
        'GC_non_work_fuel_cost_O': {},
        'GC_work_non_fuel_A': {},
        'GC_work_non_fuel_A_O': {},
        'GC_work_non_fuel_O': {},
        'GC_non_work_non_fuel_A': {},
        'GC_non_work_non_fuel_A_O': {},
        'GC_non_work_non_fuel_O': {},
        'GC_journey_time_A': {},
        'GC_journey_time_A_O': {},
        'GC_journey_time_O': {},
        'GC_emission_A': {},
        'GC_emission_A_O': {},
        'GC_emission_O': {},
        'fuel_work_benefit': {},
        'non_fuel_work_benefit': {},
        'fuel_non_work_benefit': {},
        'non_fuel_non_work_benefit': {},
        'indirect_tax_revenue': {},
        'journey_time_work_benefit': {},
        'journey_time_non_work_benefit': {},
        'emission_benefit': {},
        'all_benefit': {},
        'construction_cost_A': None,
        'maintenance_cost_A': {}
    }
        for year in range(2031, 2091):
            self.update_costs_benefits_for_year(year, self.costs_benefits)
        self.cash_flow = self.build_cash_flows(self.costs_benefits['all_benefit'], self.costs_benefits['maintenance_cost_A'], self.costs_benefits['construction_cost_A'])
        self.financial_metrics = self.calculate_financial_metrics(self.cash_flow, \
                                self.costs_benefits['all_benefit'], self.costs_benefits['maintenance_cost_A'])    
    
    def get_petrol_consumption(self, average_speed, road_length):
        return (0.45195 / average_speed + 0.09605 - 0.00109 * average_speed + 0.000007 * average_speed ** 2) * road_length

    def get_GC_emission(self, year, average_speed, road_length):
        return self.petorl_kg_per_litre * self.get_petrol_consumption(average_speed, road_length) *\
         self.data_dict[year]['money_value_of_emission'] * 1.5893 / 1000 # kg to tonne
    
    def get_work_fuel_price(self, year, average_speed):
        fuel_price_dict = {65 : self.data_dict[year]['petrol_fuel_price_65'],
                           28 : self.data_dict[year]['petrol_fuel_price_28'],
                           22 : self.data_dict[year]['petrol_fuel_price_22']}
        
        return fuel_price_dict[average_speed]
    
    def get_non_work_fuel_price(self, year, average_speed):
        fuel_price_dict = {65 : self.data_dict[year]['non_work_petrol_fuel_price_65'],
                           28 : self.data_dict[year]['non_work_petrol_fuel_price_28'],
                           22 : self.data_dict[year]['non_work_petrol_fuel_price_22']}
        return fuel_price_dict[average_speed]
    
    def get_GC_fuel(self, year, road_length, average_speed, charge_VAT = False):
        if charge_VAT:
            return self.get_non_work_fuel_price(year, average_speed) * road_length * (1 + self.vat) / 100
        else:
            return self.get_work_fuel_price(year, average_speed) * road_length / 100
        
    def get_GC_work_non_fuel(self, road_length, average_speed):
        return (4.966 + 135.946 / average_speed ) * road_length / 100
    
    def get_GC_non_work_non_fuel(self, road_length):
        return 3.846 * road_length / 100

    def update_costs_benefits_for_year(self, year, costs_benefits):
        # 更新工作时候的燃料成本，这里因为方法的参数有所变化，所以需要修改
        costs_benefits['GC_work_fuel_cost_A'][year] = self.get_GC_fuel(year, self.road_length_A, self.average_speed_A)
        costs_benefits['GC_work_fuel_cost_A_O'][year] = self.get_GC_fuel(year, self.road_length_O, self.average_speed_A_O)
        costs_benefits['GC_work_fuel_cost_O'][year] = self.get_GC_fuel(year, self.road_length_O, self.average_speed_O)
        # 更新非工作时候的燃料成本, 考虑了VAT，这里因为方法的参数有所变化，所以需要修改
        costs_benefits['GC_non_work_fuel_cost_A'][year] = self.get_GC_fuel(year, self.road_length_A, self.average_speed_A ,True)
        costs_benefits['GC_non_work_fuel_cost_A_O'][year] = self.get_GC_fuel(year, self.road_length_O, self.average_speed_A_O, True)
        costs_benefits['GC_non_work_fuel_cost_O'][year] = self.get_GC_fuel(year, self.road_length_O, self.average_speed_O, True)

        # 更新工作时非燃料成本
        costs_benefits['GC_work_non_fuel_A'][year] = self.get_GC_work_non_fuel(self.average_speed_A, self.road_length_A)
        costs_benefits['GC_work_non_fuel_A_O'][year] = self.get_GC_work_non_fuel(self.average_speed_A_O, self.road_length_A)
        costs_benefits['GC_work_non_fuel_O'][year] = self.get_GC_work_non_fuel(self.average_speed_O, self.road_length_O)

        # 更新非工作时非燃料成本，这里因为方法的参数有所变化，所以需要修改
        costs_benefits['GC_non_work_non_fuel_A'][year] = self.get_GC_non_work_non_fuel(self.road_length_A)
        costs_benefits['GC_non_work_non_fuel_A_O'][year] = self.get_GC_non_work_non_fuel(self.road_length_A)
        costs_benefits['GC_non_work_non_fuel_O'][year] = self.get_GC_non_work_non_fuel(self.road_length_O)

        # 更新旅行时间成本
        costs_benefits['GC_journey_time_A'][year] = self.get_GC_journey_time(year, self.average_speed_A, self.road_length_A)
        costs_benefits['GC_journey_time_A_O'][year] = self.get_GC_journey_time(year, self.average_speed_A_O, self.road_length_O)
        costs_benefits['GC_journey_time_O'][year] = self.get_GC_journey_time(year, self.average_speed_O, self.road_length_O)

        # 更新排放成本,因为方法的参数有所变化，所以需要修改
        costs_benefits['GC_emission_A'][year] = self.get_GC_emission(year, self.average_speed_A, self.road_length_A)
        costs_benefits['GC_emission_A_O'][year] = self.get_GC_emission(year, self.average_speed_A_O, self.road_length_A)
        costs_benefits['GC_emission_O'][year] = self.get_GC_emission(year, self.average_speed_O, self.road_length_O)

        # 更新收益
        w, nw = 0.053, 0.947  # 权重值
        costs_benefits['fuel_work_benefit'][year] = self.get_benefit_by_ROH(year, costs_benefits['GC_work_fuel_cost_A'][year], \
                                                    costs_benefits['GC_work_fuel_cost_A_O'][year], costs_benefits['GC_work_fuel_cost_O'][year], w, True)
        costs_benefits['non_fuel_work_benefit'][year] = self.get_benefit_by_ROH(year, costs_benefits['GC_work_non_fuel_A'][year], \
                                                    costs_benefits['GC_work_non_fuel_A_O'][year], costs_benefits['GC_work_non_fuel_O'][year], w, True)
        costs_benefits['fuel_non_work_benefit'][year] = self.get_benefit_by_ROH(year, costs_benefits['GC_non_work_fuel_cost_A'][year], \
                                                    costs_benefits['GC_non_work_fuel_cost_A_O'][year], costs_benefits['GC_non_work_fuel_cost_O'][year], nw)
        costs_benefits['non_fuel_non_work_benefit'][year] = self.get_benefit_by_net(year, costs_benefits['GC_non_work_non_fuel_A'][year],\
                                                            costs_benefits['GC_non_work_non_fuel_A_O'][year], costs_benefits['GC_non_work_non_fuel_O'][year], nw)
        costs_benefits['journey_time_work_benefit'][year] = self.get_benefit_by_ROH(year, costs_benefits['GC_journey_time_A'][year], \
                                                            costs_benefits['GC_journey_time_A_O'][year], costs_benefits['GC_journey_time_O'][year], w, True)
        costs_benefits['journey_time_non_work_benefit'][year] = self.get_benefit_by_ROH(year, costs_benefits['GC_journey_time_A'][year], \
                                                            costs_benefits['GC_journey_time_A_O'][year], costs_benefits['GC_journey_time_O'][year], nw)
        
        costs_benefits['emission_benefit'][year] = self.get_benefit_by_net(year, costs_benefits['GC_emission_A'][year], costs_benefits['GC_emission_A_O'][year], costs_benefits['GC_emission_O'][year], 1)

        # 间接税收入、维护成本和建设成本的更新
        costs_benefits['indirect_tax_revenue'][year] = self.get_GC_indirect_tax(year, costs_benefits['fuel_work_benefit'], costs_benefits['non_fuel_work_benefit'], costs_benefits['fuel_non_work_benefit'], costs_benefits['non_fuel_non_work_benefit'])
        costs_benefits['maintenance_cost_A'][year] = self.get_maintenance_cost()
        costs_benefits['construction_cost_A'] = self.get_construction_cost()
        costs_benefits['all_benefit'][year] = costs_benefits['fuel_work_benefit'][year] + costs_benefits['non_fuel_work_benefit'][year] + \
                                            costs_benefits['fuel_non_work_benefit'][year] + costs_benefits['non_fuel_non_work_benefit'][year] \
                                            + costs_benefits['indirect_tax_revenue'][year] + costs_benefits['journey_time_work_benefit'][year] + \
                                                costs_benefits['journey_time_non_work_benefit'][year] + costs_benefits['emission_benefit'][year]
            

if __name__ == '__main__':
    schemeB1 = EcoPetrol('voc.csv', road_length_A = 11, \
        AADT_A=13500, AADT_A_O=3500, construction_cost_A=77000000, maintenance_cost_A=10000, growth_rate = 0.01)
    print(schemeB1.financial_metrics)
    schemeA1 = EcoPetrol()
    print(schemeA1.financial_metrics)
    schemeA1.save_data_to_excel('eco_petrol.xlsx')