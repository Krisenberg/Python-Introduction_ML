import pandas as pd
from pathlib import Path  

data_dir_path = "C:\\Users\\Kris\\Documents\\Studia\\Semestr_IV\\MSiD_L\\Project\\Data\\Portugal\\"

gdpFile = data_dir_path + 'GDP.csv'
inflationFile = data_dir_path + 'Inflation.csv'
unempFile = data_dir_path + 'Unemployment.csv'
interestRatesFile = data_dir_path + 'InterestRates.csv'
stockIndexFile = data_dir_path + 'StockIndex.csv'
mergedFile = data_dir_path + 'Portugal_data.csv'

def GDPToCsv():
    global gdpFile
    global data_dir_path
    data = pd.read_csv(gdpFile)
    filteredData = [data['Series;Series description (EN);Metric;Unit of Measure;Reference date;Value;State'][index].split(';')[5] for index in range(20)]
    preparedData = pd.DataFrame([float(filteredData[i])/3 for i in range(len(filteredData)) for _ in range(3)])
    filepath = Path(data_dir_path + '1.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def InflationToCsv():
    global inflationFile
    global data_dir_path
    data = pd.read_csv(inflationFile)
    filteredData = [data['Series;Series description (EN);Metric;Unit of Measure;Reference date;Value;State'][index].split(';')[5] for index in range(60)]
    preparedData = pd.DataFrame(filteredData)
    filepath = Path(data_dir_path + '2.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def unemploymentToCsv():
    global unempFile
    global data_dir_path
    data = pd.read_csv(unempFile)
    filteredData = [data['Series;Series description (EN);Metric;Unit of Measure;Reference date;Value;State'][index].split(';')[5] for index in range(20)]
    preparedData = pd.DataFrame([filteredData[i] for i in range(len(filteredData)) for _ in range(3)])
    filepath = Path(data_dir_path + '3.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def interestRatesToCsv():
    global interestRatesFile
    global data_dir_path
    data = pd.read_csv(interestRatesFile)
    indexStart = 0
    indexEnd = 0
    for i in range(len(data['date'])):
        if data['date'][i]=='2018-01-31':
            indexStart = i
        if data['date'][i]=='2022-12-31':
            indexEnd = i
    filteredData = [data['s1'][index] for index in range(indexStart, indexEnd+1)]
    preparedData = pd.DataFrame(filteredData)
    filepath = Path(data_dir_path + '4.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def stockIndexToCsv():
    global stockIndexFile
    global data_dir_path
    data = pd.read_csv(stockIndexFile)
    filteredData = [(100 * float(data['Adj Close'][index])/float(data['Adj Close'][index-1]))-100 for index in range(1,61)]
    preparedData = pd.DataFrame(filteredData)
    filepath = Path(data_dir_path + '5.csv')
    preparedData.to_csv(filepath, index=False, header=False)
    

def mergeData():
    global mergedFile
    global data_dir_path

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