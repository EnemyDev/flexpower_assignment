import csv
from pathlib import Path

data_folder = (Path(__file__).parent.absolute() / "../../data").resolve()

def strip_and_replace_dot(column):
    return column.replace(' ','').replace(',','.')

def clean_csv():
    i = 0
    output_file = open(f'{data_folder}/processed/cleaned.csv', "w")
    with open(data_folder / 'raw/DE_Wind_PV_Prices.csv') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            line = ''
            if(i==0):
                for col in row:
                    line += f"{col}" if line == '' else f",{col}"
            else:
                for col in row:
                    line += f"{strip_and_replace_dot(col)}" if line == '' else f",{strip_and_replace_dot(col)}" 
            output_file.write(f"{line}\n")
            i+=1
    output_file.close()
