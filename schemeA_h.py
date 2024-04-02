from eco import TransportationScheme
import pandas as pd

# 假设你的CSV文件位于这个路径
csv_file_path = 'voc.csv'

# 创建TransportationScheme类的实例
scheme_A = TransportationScheme(csv_file_path, growth_rate=0.02)

# 获取所有的感知成本
GC_fuel_cost_A = {}
GC_fuel_cost_A_O = {}
GC_fuel_cost_O = {}
GC_work_non_fuel_A = {}
GC_work_non_fuel_A_O = {}
GC_work_non_fuel_O = {}
GC_non_work_non_fuel_A = {}
GC_non_work_non_fuel_A_O = {}
GC_non_work_non_fuel_O = {}
GC_journey_time_A = {}
GC_journey_time_A_O = {}
GC_journey_time_O = {}
GC_emission_A = {}
GC_emission_A_O = {}
GC_emission_O = {}
# 获取所有的收益
fuel_work_benefit = {}
non_fuel_work_benefit = {}
fuel_non_work_benefit = {}
non_fuel_non_work_benefit = {}
indirect_tax_revenue = {}
journey_time_benefit = {}
emission_benefit = {}
all_benefit = {}
# 获取成本
construction_cost_A = {}
maintenance_cost_A = {}
# 计算权重
w =  0.053
nw = 0.947
for year in range(2031, 2091):
    GC_fuel_cost_A[year] = scheme_A.get_GC_fuel(year, scheme_A.road_length_A)
    GC_fuel_cost_A_O[year] = scheme_A.get_GC_fuel(year, scheme_A.road_length_O)
    GC_fuel_cost_O[year] = scheme_A.get_GC_fuel(year, scheme_A.road_length_O)
    GC_work_non_fuel_A[year] = scheme_A.get_GC_work_non_fuel(scheme_A.average_speed_A, scheme_A.road_length_A)
    GC_work_non_fuel_A_O[year] = scheme_A.get_GC_work_non_fuel(scheme_A.average_speed_A_O, scheme_A.road_length_A)
    GC_work_non_fuel_O[year] = scheme_A.get_GC_work_non_fuel(scheme_A.average_speed_O, scheme_A.road_length_O)
    GC_non_work_non_fuel_A[year] = scheme_A.get_GC_non_work_non_fuel(scheme_A.average_speed_A, scheme_A.road_length_A)
    GC_non_work_non_fuel_A_O[year] = scheme_A.get_GC_non_work_non_fuel(scheme_A.average_speed_A_O, scheme_A.road_length_A)
    GC_non_work_non_fuel_O[year] = scheme_A.get_GC_non_work_non_fuel(scheme_A.average_speed_O, scheme_A.road_length_O)
    GC_journey_time_A[year] = scheme_A.get_GC_journey_time(year, scheme_A.average_speed_A, scheme_A.road_length_A)
    GC_journey_time_A_O[year] = scheme_A.get_GC_journey_time(year, scheme_A.average_speed_A_O, scheme_A.road_length_O)
    GC_journey_time_O[year] = scheme_A.get_GC_journey_time(year, scheme_A.average_speed_O, scheme_A.road_length_O)
    GC_emission_A[year] = scheme_A.get_GC_emission(year, scheme_A.road_length_A)
    GC_emission_A_O[year] = scheme_A.get_GC_emission(year, scheme_A.road_length_O)
    GC_emission_O[year] = scheme_A.get_GC_emission(year, scheme_A.road_length_O)
    fuel_work_benefit[year] = scheme_A.get_benefit_by_ROH(year, GC_fuel_cost_A[year], GC_fuel_cost_A_O[year], GC_fuel_cost_O[year], w)
    non_fuel_work_benefit[year] = scheme_A.get_benefit_by_ROH(year, GC_work_non_fuel_A[year], GC_work_non_fuel_A_O[year], GC_work_non_fuel_O[year], w)
    fuel_non_work_benefit[year] = scheme_A.get_benefit_by_ROH(year, GC_fuel_cost_A[year], GC_fuel_cost_A_O[year], GC_fuel_cost_O[year], nw)
    non_fuel_non_work_benefit[year] = scheme_A.get_benefit_by_net(year, GC_non_work_non_fuel_A[year], GC_non_work_non_fuel_A_O[year], GC_non_work_non_fuel_O[year], nw)
    indirect_tax_revenue[year] = scheme_A.get_GC_indirect_tax(year, fuel_work_benefit, non_fuel_work_benefit, fuel_non_work_benefit, non_fuel_non_work_benefit)
    journey_time_benefit[year] = scheme_A.get_benefit_by_ROH(year, GC_journey_time_A[year], GC_journey_time_A_O[year], GC_journey_time_O[year], 1)
    emission_benefit[year] = scheme_A.get_benefit_by_net(year, GC_emission_A[year], GC_emission_A_O[year], GC_emission_O[year], 1)
    construction_cost_A = scheme_A.get_construction_cost() 
    maintenance_cost_A[year] = scheme_A.get_maintenance_cost()
    all_benefit[year] = fuel_work_benefit[year] + non_fuel_work_benefit[year] + fuel_non_work_benefit[year] + \
                        non_fuel_non_work_benefit[year] - indirect_tax_revenue[year] + journey_time_benefit[year] + emission_benefit[year]


cash_flows = scheme_A.build_cash_flows(all_benefit, maintenance_cost_A, construction_cost_A)
# 计算PVB, PVC, NPV, BCR, IRR, Payback Period, First Year Rate of Return
scheme_PVB = scheme_A.get_PVB(all_benefit, 2090)
scheme_PVC = scheme_A.get_PVC(maintenance_cost_A, construction_cost_A, 2090)
scheme_NPV = scheme_A.get_NPV(all_benefit, maintenance_cost_A, construction_cost_A, 2090)
scheme_BCR = scheme_PVB / scheme_PVC
scheme_IRR = scheme_A.get_IRR(cash_flows)
scheme_PP = scheme_A.get_payback_period(all_benefit, maintenance_cost_A, construction_cost_A)
scheme_FYRR = scheme_A.get_FYRR(all_benefit, maintenance_cost_A, construction_cost_A)

# 整理成字典
data = {
    'Year': list(all_benefit.keys()),  # 年份
    'Fuel Work Benefit': list(fuel_work_benefit.values()),
    'Non-fuel Work Benefit': list(non_fuel_work_benefit.values()),
    'Fuel Non-work Benefit': list(fuel_non_work_benefit.values()),
    'Non-fuel Non-work Benefit': list(non_fuel_non_work_benefit.values()),
    'Indirect Tax Revenue': list(indirect_tax_revenue.values()),
    'Journey Time Benefit': list(journey_time_benefit.values()),
    'Emission Benefit': list(emission_benefit.values()),
    'Total Benefit': list(all_benefit.values()),
    'Maintenance Cost': list(maintenance_cost_A.values()),
    'Construction Cost': [construction_cost_A if year == list(all_benefit.keys())[0] else None for year in all_benefit],  # 假设建设成本是在第一年支付
}

# 转换成DataFrame
results_df = pd.DataFrame(data)

# 计算指标的结果
summary_data = {
    'PVB': [scheme_PVB],
    'PVC': [scheme_PVC],
    'NPV': [scheme_NPV],
    'BCR': [scheme_BCR],
    'IRR': [scheme_IRR],
    'Payback Period': [scheme_PP],
    'First Year Rate of Return': [scheme_FYRR]
}

summary_df = pd.DataFrame(summary_data)

# 使用ExcelWriter保存DataFrame到xlsx
with pd.ExcelWriter('TransportationSchemeResultsA2.xlsx') as writer:
    # 将结果DataFrame保存到一个工作表
    results_df.to_excel(writer, sheet_name='Benefits and Costs', index=False)
    # 将汇总指标DataFrame保存到另一个工作表
    summary_df.to_excel(writer, sheet_name='Financial Indicators', index=False)

print('数据已成功保存到Excel文件。')
