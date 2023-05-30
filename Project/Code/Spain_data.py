import pandas as pd
from pathlib import Path 
import numpy as np 

data_dir_path = "C:\\Users\\Kris\\Documents\\Studia\\Semestr_IV\\MSiD_L\\Project\\Data\\Spain\\"

gdpFile = data_dir_path + 'GDP.csv'
inflationFile = data_dir_path + 'Inflation.csv'
unempFile = data_dir_path + 'Unemployment.csv'
interestRatesFile = data_dir_path + 'InterestRates.csv'
stockIndexFile = data_dir_path + 'StockIndex.csv'
mergedFile = data_dir_path + 'Spain_data.csv'

def GDPToCsv():
    data = pd.read_csv(gdpFile)
    start_index = data['TIME'].values.tolist().index('2018-Q1')
    stop_index = data['TIME'].values.tolist().index('2022-Q4')
    filteredData = [data['Value'][i] for i in range (start_index, stop_index+1)]
    preparedData = pd.DataFrame([(100 * np.cbrt((100 + float(filteredData[i]))/100))-100 for i in range(len(filteredData)) for _ in range(3)])
    filepath = Path(data_dir_path + '1.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def InflationToCsv():
    data = pd.read_csv(inflationFile, sep=';')
    start_index = data['PERIODO'].values.tolist().index('2018M01')
    stop_index = data['PERIODO'].values.tolist().index('2022M12')
    filteredData = [float(data['VALOR'][i].replace(',','.')) for i in range (start_index, stop_index-1, -1)]
    preparedData = pd.DataFrame(filteredData)
    filepath = Path(data_dir_path + '2.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def unemploymentToCsv():
    data = pd.read_csv(unempFile)
    start_index = data['TIME'].values.tolist().index('2018-01')
    stop_index = data['TIME'].values.tolist().index('2022-12')
    filteredData = [((100 * float(data['Value'][i]))/float(data['Value'][i-1]))-100 for i in range (start_index, stop_index+1)]
    preparedData = pd.DataFrame(filteredData)
    filepath = Path(data_dir_path + '3.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def interestRatesToCsv():
    data = pd.read_csv(interestRatesFile)    
    start_index = data['date'].values.tolist().index('2018-01-31')
    stop_index = data['date'].values.tolist().index('2022-12-31')
    filteredData = [data['s1'][index] for index in range(start_index, stop_index+1)]
    preparedData = pd.DataFrame(filteredData)
    filepath = Path(data_dir_path + '4.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def stockIndexToCsv():
    data = pd.read_csv(stockIndexFile)
    filteredData = [(100 * float(data['Adj Close'][index])/float(data['Adj Close'][index-1]))-100 for index in range(1,len(data))]
    preparedData = pd.DataFrame(filteredData)
    filepath = Path(data_dir_path + '5.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def mergeData():
    merged_df = pd.DataFrame()
    for i in range(1,6):
        file_path = data_dir_path + (f"{i}.csv")
        temp_df = pd.read_csv(file_path, header=None)
        merged_df = pd.concat([merged_df, temp_df], axis=1)

    headers = ['GDP change (%)', 'Inflation (%)', 'Unemployment rate (%)', 'Interest rates (%)', 'Stock Index change (%)']
    merged_df.to_csv(mergedFile, index=False, header=headers)


if __name__ == "__main__":
    GDPToCsv()
    InflationToCsv()
    unemploymentToCsv()
    interestRatesToCsv()
    stockIndexToCsv()
    mergeData()
    


