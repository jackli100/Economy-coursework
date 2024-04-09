from eco_petrol import TransportationScheme
from eco import TransportationScheme
import csv

def process_csv_column(input_csv_path, multiplier):
    # 构造输出文件路径
    parts = input_csv_path.rsplit('.', 1)
    output_csv_path = f'{parts[0]}_processed.{parts[1]}'

    # 读取CSV文件，并处理第四列
    with open(input_csv_path, mode='r', encoding='utf-8') as infile, \
         open(output_csv_path, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 首先复制标题行
        writer.writerow(next(reader))

        # 遍历剩下的行，处理第五列
        for row in reader:
            if len(row) > 4:  # 确保行中有足够的列
                row[4] = str(float(row[4]) * multiplier)  # 将第五列的值乘以指定的系数
            writer.writerow(row)

    # 处理完成
    print(f'CSV文件已处理完成并保存为: {output_csv_path}')
result_dict ={}

def sensitive_analysis():
    SchemeA1 = TransportationScheme('voc.csv')
    SchemeA1.get_things_done()
    SchemeA2 = TransportationScheme('voc.csv', growth_rate=0.02)
    schemeB1 = TransportationScheme('voc.csv', road_length_A = 11, \
            AADT_A=13500, AADT_A_O=3500, construction_cost_A=77000000, maintenance_cost_A=10000)
    schemeB2 = TransportationScheme('voc.csv', road_length_A = 11, \
            AADT_A=13500, AADT_A_O=3500, construction_cost_A=77000000, maintenance_cost_A=10000, growth_rate = 0.02)
    result_original = SchemeA1.financial_metrics
    result_dict['original'] = result_original
    optimism_bias_uplifts = 1.46
    # 分析资本成本的敏感性
    constuction_cost_uplifts_A = 1.46 * 90000000
    constuction_cost_uplifts_B = 1.46 * 77000000
    SchemeA1_2 = TransportationScheme('voc.csv', construction_cost_A=1.46 * 90000000)
    SchemeA1_2.get_things_done()
    result_construciton = SchemeA1_2.financial_metrics
    result_dict['construciton'] = result_construciton
    # 分析时间价值
    SchemeA1_3 = TransportationScheme('voc.csv', value_of_time = 10.79 / 1.46, growth_rate=0.02)
    SchemeA1_3.get_things_done()
    result_time_value = SchemeA1_3.financial_metrics
    result_dict['time_value'] = result_time_value
    # the value of Greenhouse Gas emissions
    # 分析排放成本
    process_csv_column('voc.csv', 1.46)
    SchemeA1_4 = TransportationScheme('voc_processed.csv')
    SchemeA1_4.get_things_done()

    result_emission = SchemeA1_4.financial_metrics
    result_dict['emission'] = result_emission
    # 分析项目寿命
    SchemeA1_5 = TransportationScheme('voc.csv', project_life = int(60 / 1.46))
    SchemeA1_5.get_things_done()
    result_project_life = SchemeA1_5.financial_metrics
    result_dict['project_life'] = result_project_life

    # 分析折扣率
    SchemeA1_6 = TransportationScheme('voc.csv', discount_rate_1 = 0.035 * 1.46, discount_rate_2 = 0.03 * 1.46)
    SchemeA1_6.get_things_done()
    result_discount_rate = SchemeA1_6.financial_metrics
    result_dict['discount_rate'] = result_discount_rate

    return result_dict

if __name__ == '__main__':
    sensitive_analysis()
    for key, value in result_dict.items():
        print(f"{key}: {value}")
