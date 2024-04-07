from eco import TransportationScheme

class EcoPetrol(TransportationScheme):

    def __init__(self, csv_file_path = 'voc.csv', petrol_consumption_csv = 'petrol_consumption.csv', transport_scheme_name = 'A_low', value_of_time = 10.79, road_length_O=5, average_speed_O=22, AADT_O=15000,
                 road_length_A=9, average_speed_A=65, average_speed_A_O=28, AADT_A=13000,
                 AADT_A_O=4000, construction_cost_A=90000000, maintenance_cost_A=10000, growth_rate = 0.01, VAT = 0.2, project_life = 60,
                 discount_rate_1 = 0.035, discount_rate_2 = 0.03, petorl_kg_per_litre = 2.11):
        self.csv_file_path = csv_file_path
        super().__init__(csv_file_path, transport_scheme_name, value_of_time, road_length_O, average_speed_O, AADT_O, road_length_A, 
                         average_speed_A, average_speed_A_O, AADT_A, AADT_A_O, construction_cost_A, maintenance_cost_A, growth_rate, VAT,
                           project_life, discount_rate_1, discount_rate_2)
        self.tf = 0.2
        self.petorl_kg_per_litre = petorl_kg_per_litre
        self.petrol_consumption_csv = petrol_consumption_csv
        self.petrol_consumption = {}
        self.load_petrol_consumption()
        
    def load_petrol_consumption(self): 
        for year in range(2031, 2091):
            self.petrol_consumption[year] = {'65': None, '28': None, '22': None}
        with open(self.petrol_consumption_csv, 'r', encoding='utf-8-sig') as f: 
            # 读取文件，第一列是65km/h的燃油消耗，第二列是28km/h的燃油消耗，第三列是22km/h的燃油消耗,行数加上2030是年份
            year = 2031
            for line in f:
                # 假设每行数据是逗号分隔的
                consumption_values = line.strip().split(',')
                if len(consumption_values) == 3:  # 确保每行有三个数据
                    # 更新对应年份的燃油消耗数据
                    self.petrol_consumption[year]['65'] = float(consumption_values[0])
                    self.petrol_consumption[year]['28'] = float(consumption_values[1])
                    self.petrol_consumption[year]['22'] = float(consumption_values[2])
                year += 1  # 移到下一个年份

    def get_GC_emission(self, year, average_speed, road_length):
        return self.petorl_kg_per_litre * self.petrol_consumption[year][str(average_speed)] *\
         self.data_dict[year]['money_value_of_emission'] * road_length * 1.5893 / 1000 # kg to tonne
    
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
    
    def get_GC_fuel(self, year, road_length, average_speed, non_work = False):
        '''
        计算燃料成本，单位是英镑每公里
        
        公式中get_non_work_fuel_price和get_work_fuel_price是燃料价格，单位是便士每公里，需要转换为英镑每升
        需要对于非工作时间的燃料成本收取VAT，但是已经包含在内了，所以不需要再次计算
        
        Parameters:
        ----------
        param year: int
            年份
        param road_length: float
            路段长度

        Returns:
        -------
        float: 特定道路的燃料成本
        '''
        # 需要对非工作收取VAT
        if non_work:
            return self.get_non_work_fuel_price(year, average_speed) * road_length / 100
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
        # 更新非工作时候的燃料成本，这里因为方法的参数有所变化，所以需要修改
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
    schemeA1 = TransportationScheme()
    schemeA1.get_things_done()
    print(schemeA1.financial_metrics)
    schemeB1 = EcoPetrol()
    schemeB1.get_things_done()
    print(schemeB1.financial_metrics)