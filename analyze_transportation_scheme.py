import pandas as pd
from eco import TransportationScheme

def discount_to_2030(values, end_year):
    """
    对给定的每年收益按年折现到2030年。
    对于距2030年30年内的年份使用3.5%的折现率，超过30年的部分使用3%的折现率。
    
    参数:
    values: 一个字典，键为年份，值为那一年的收益。
    
    返回:
    2030年的折现总值。
    """
    discount_value = 0  # 初始化折现后的总值
    for year, value in values.items():
        if year > end_year:
            continue

        years_diff = year - 2030  # 计算与2030年的年差
        if years_diff <= 30:
            # 对于30年及以内的部分，使用3.5%的折现率
            discount_factor = (1 + 0.035) ** years_diff
        else:
            # 对于超过30年的部分，前30年使用3.5%，之后使用3%
            discount_factor_30 = (1 + 0.035) ** 30
            discount_factor_after_30 = (1 + 0.03) ** (years_diff - 30)
            discount_factor = discount_factor_30 * discount_factor_after_30
        
        discount_value += value / discount_factor  # 将该年的收益折现到2030年的价值，并累加到总值中
    
    return discount_value

def analyze_transportation_scheme(scheme, output_file='A_low.xlsx'):
    # 获取所有的感知成本和收益
    costs_benefits = {
        'GC_fuel_cost_A': {},
        'GC_fuel_cost_A_O': {},
        'GC_fuel_cost_O': {},
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
        'journey_time_benefit': {},
        'emission_benefit': {},
        'all_benefit': {},
        'construction_cost_A': None,
        'maintenance_cost_A': {}
    }
    for year in range(2031, 2091):
        update_costs_benefits_for_year(scheme, year, costs_benefits)

    cash_flows = scheme.build_cash_flows(costs_benefits['all_benefit'], costs_benefits['maintenance_cost_A'], costs_benefits['construction_cost_A'])
    # 计算PVB, PVC, NPV, BCR, IRR, Payback Period, First Year Rate of Return
    financial_metrics = scheme.calculate_financial_metrics(cash_flows, costs_benefits['all_benefit'], costs_benefits['maintenance_cost_A'])
    
    # 整理数据，准备写入Excel
    data, summary_data = prepare_data_for_excel(costs_benefits, financial_metrics)

    save_to_excel(data, summary_data, output_file)

def update_costs_benefits_for_year(scheme, year, costs_benefits):
    # 更新燃料成本
    costs_benefits['GC_fuel_cost_A'][year] = scheme.get_GC_fuel(year, scheme.road_length_A)
    costs_benefits['GC_fuel_cost_A_O'][year] = scheme.get_GC_fuel(year, scheme.road_length_O)
    costs_benefits['GC_fuel_cost_O'][year] = scheme.get_GC_fuel(year, scheme.road_length_O)

    # 更新工作时非燃料成本
    costs_benefits['GC_work_non_fuel_A'][year] = scheme.get_GC_work_non_fuel(scheme.average_speed_A, scheme.road_length_A)
    costs_benefits['GC_work_non_fuel_A_O'][year] = scheme.get_GC_work_non_fuel(scheme.average_speed_A_O, scheme.road_length_A)
    costs_benefits['GC_work_non_fuel_O'][year] = scheme.get_GC_work_non_fuel(scheme.average_speed_O, scheme.road_length_O)

    # 更新非工作时非燃料成本
    costs_benefits['GC_non_work_non_fuel_A'][year] = scheme.get_GC_non_work_non_fuel(scheme.average_speed_A, scheme.road_length_A)
    costs_benefits['GC_non_work_non_fuel_A_O'][year] = scheme.get_GC_non_work_non_fuel(scheme.average_speed_A_O, scheme.road_length_A)
    costs_benefits['GC_non_work_non_fuel_O'][year] = scheme.get_GC_non_work_non_fuel(scheme.average_speed_O, scheme.road_length_O)

    # 更新旅行时间成本
    costs_benefits['GC_journey_time_A'][year] = scheme.get_GC_journey_time(year, scheme.average_speed_A, scheme.road_length_A)
    costs_benefits['GC_journey_time_A_O'][year] = scheme.get_GC_journey_time(year, scheme.average_speed_A_O, scheme.road_length_O)
    costs_benefits['GC_journey_time_O'][year] = scheme.get_GC_journey_time(year, scheme.average_speed_O, scheme.road_length_O)

    # 更新排放成本
    costs_benefits['GC_emission_A'][year] = scheme.get_GC_emission(year, scheme.road_length_A)
    costs_benefits['GC_emission_A_O'][year] = scheme.get_GC_emission(year, scheme.road_length_O)
    costs_benefits['GC_emission_O'][year] = scheme.get_GC_emission(year, scheme.road_length_O)

    # 更新收益
    w, nw = 0.053, 0.947  # 权重值
    costs_benefits['fuel_work_benefit'][year] = scheme.get_benefit_by_ROH(year, costs_benefits['GC_fuel_cost_A'][year], costs_benefits['GC_fuel_cost_A_O'][year], costs_benefits['GC_fuel_cost_O'][year], w)
    costs_benefits['non_fuel_work_benefit'][year] = scheme.get_benefit_by_ROH(year, costs_benefits['GC_work_non_fuel_A'][year], costs_benefits['GC_work_non_fuel_A_O'][year], costs_benefits['GC_work_non_fuel_O'][year], w)
    costs_benefits['fuel_non_work_benefit'][year] = scheme.get_benefit_by_ROH(year, costs_benefits['GC_fuel_cost_A'][year], costs_benefits['GC_fuel_cost_A_O'][year], costs_benefits['GC_fuel_cost_O'][year], nw)
    costs_benefits['non_fuel_non_work_benefit'][year] = scheme.get_benefit_by_net(year, costs_benefits['GC_non_work_non_fuel_A'][year], costs_benefits['GC_non_work_non_fuel_A_O'][year], costs_benefits['GC_non_work_non_fuel_O'][year], nw)
    costs_benefits['journey_time_benefit'][year] = scheme.get_benefit_by_ROH(year, costs_benefits['GC_journey_time_A'][year], costs_benefits['GC_journey_time_A_O'][year], costs_benefits['GC_journey_time_O'][year], 1)
    costs_benefits['emission_benefit'][year] = scheme.get_benefit_by_net(year, costs_benefits['GC_emission_A'][year], costs_benefits['GC_emission_A_O'][year], costs_benefits['GC_emission_O'][year], 1)

    # 间接税收入、维护成本和建设成本的更新
    costs_benefits['indirect_tax_revenue'][year] = scheme.get_GC_indirect_tax(year, costs_benefits['fuel_work_benefit'], costs_benefits['non_fuel_work_benefit'], costs_benefits['fuel_non_work_benefit'], costs_benefits['non_fuel_non_work_benefit'])
    costs_benefits['maintenance_cost_A'][year] = scheme.get_maintenance_cost()
    costs_benefits['construction_cost_A'] = scheme.get_construction_cost()
    costs_benefits['all_benefit'][year] = costs_benefits['fuel_work_benefit'][year] + costs_benefits['non_fuel_work_benefit'][year] + \
                                        costs_benefits['fuel_non_work_benefit'][year] + costs_benefits['non_fuel_non_work_benefit'][year] \
                                        - costs_benefits['indirect_tax_revenue'][year] + costs_benefits['journey_time_benefit'][year] + \
                                        costs_benefits['emission_benefit'][year]
    
def prepare_data_for_excel(costs_benefits, financial_metrics):
    
    data = {'Year': list(costs_benefits['all_benefit'].keys()),
            'Fuel Work Benefit': list(costs_benefits['fuel_work_benefit'].values()),
            'Non Fuel Work Benefit': list(costs_benefits['non_fuel_work_benefit'].values()),
            'Fuel Non Work Benefit': list(costs_benefits['fuel_non_work_benefit'].values()),
            'Non Fuel Non Work Benefit': list(costs_benefits['non_fuel_non_work_benefit'].values()),
            'Indirect Tax Revenue': list(costs_benefits['indirect_tax_revenue'].values()),
            'Journey Time Benefit': list(costs_benefits['journey_time_benefit'].values()),
            'Emission Benefit': list(costs_benefits['emission_benefit'].values()),
            'All Benefit': list(costs_benefits['all_benefit'].values()),
            'Maintenance Cost': list(costs_benefits['maintenance_cost_A'].values()),
            'Construction Cost': [costs_benefits['construction_cost_A']] + [None] * (len(costs_benefits['all_benefit']) - 1)
              }
    
    summary_data = {key: [value] for key, value in financial_metrics.items()}

    return pd.DataFrame(data), pd.DataFrame(summary_data)

def save_to_excel(data, summary_data, output_file):
    with pd.ExcelWriter(output_file) as writer:
        data.to_excel(writer, sheet_name='Benefits and Costs', index=False)
        summary_data.to_excel(writer, sheet_name='Financial Indicators', index=False)


if __name__ == '__main__':
    scheme_A_low = TransportationScheme('voc.csv')
    analyze_transportation_scheme(scheme_A_low, 'A_low_2.xlsx')
    

    