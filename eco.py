import numpy as np
import pandas as pd
import csv

import csv

class CostBenefitAnalysis:

    # 这里A代指新方案，O代指旧方案
    def __init__(self, csv_file_path, road_length_O=5, average_speed_O=22, AADT_O=15000,
                 road_length_A=9, average_speed_A=65, average_speed_A_O=28, AADT_A=13000,
                 AADT_A_O=4000, construction_cost_A=90000000, maintenance_cost_A=10000):
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

        # 加载CSV文件数据
        self.data_dict = self.load_csv_data(csv_file_path)

    @staticmethod
    def load_csv_data(csv_file_path):
        """加载CSV文件数据到字典"""
        data_dict = {}
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过标题行
            for row in reader:
                year = int(row[0])
                data_dict[year] = {
                    'fuel_price_per_kwh': float(row[1]),
                    'fuel_efficiency': float(row[2]),
                    'emission_factor': float(row[3]),
                    'money_value_of_emission': float(row[4]),
                    'petrol_fuel_price_65': float(row[5]),
                    'petrol_fuel_price_28': float(row[6]),
                    'petrol_fuel_price_22': float(row[7]),
                    'non_work_petrol_fuel_price_65': float(row[8]),
                    'non_work_petrol_fuel_price_28': float(row[9]),
                    'non_work_petrol_fuel_price_22': float(row[10]),
                }
        return data_dict
    
    def get_GC_work_fuel():
        pass

    def get_GC_work_non_fuel():
        pass

    def get_GC_non_work_fuel():
        pass

    def get_GC_non_work_non_fuel():
        pass

    def get_GC_journey_time():
        pass

    def get_GC_emission():
        pass

    def get_GC_indirect_tax():
        pass

    def get_cost():
        pass
    
    def get_benefit_by_ROH():
        pass

    def get_benefit_by_net():
        pass

    def get_benefit():
        pass

    def get_NPV():
        pass
    
    def get_PVB():
        pass

    def get_PVC():
        pass

    def get_BC_ratio():
        pass

    def get_IRR():
        pass

    def get_payback_period():
        pass

    def get_FYRR():
        pass


# 假设你的CSV文件位于这个路径
csv_file_path = 'voc.csv'

# 创建TransportationScheme类的实例
scheme_instance = CostBenefitAnalysis(csv_file_path)

# 打印出一些数据来确认实例已正确加载数据
print(f"Scheme O Road Length: {scheme_instance.road_length_O} km")
print(f"Scheme A Average Speed: {scheme_instance.average_speed_A} km/h")
print(f"Data Dictionary for a specific year (e.g., 2020): {scheme_instance.data_dict.get(2031)}")
