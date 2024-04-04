from eco_petrol import EcoPetrol
from analyze_transportation_scheme2 import analyze_transportation_scheme

SchemeA1 = EcoPetrol('voc.csv')
resultA1 = analyze_transportation_scheme(SchemeA1, output_file='A_low_petrol.xlsx', write_to_excel=True)
print(resultA1)