import pandas as pd
from pathlib import Path  

data_dir_path = "C:\\Users\\Kris\\Documents\\Studia\\Semestr_IV\\MSiD_L\\Project\\Data\\Slovenia\\"

gdpFile = data_dir_path + 'GDP.csv'
inflationFile = data_dir_path + 'Inflation.csv'
unempFile = data_dir_path + 'Unemployment.csv'
interestRatesFile = data_dir_path + 'InterestRates.csv'
stockIndexFile = data_dir_path + 'StockIndex.csv'
mergedFile = data_dir_path + 'Slovenia_data.csv'

def GDPToCsv():
    global gdpFile
    global data_dir_path
    data = pd.read_csv(gdpFile)
    filteredData = [data[f"Volume growth rate compared to the previous quarter (%) Seasonally adjusted data 20{year}Q{q}"][0] for year in range(18,23) for q in range(1,5)]
    preparedData = pd.DataFrame([filteredData[i]/3 for i in range(len(filteredData)) for _ in range(3)])
    filepath = Path(data_dir_path + '1.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def InflationToCsv():
    global inflationFile
    global data_dir_path
    data = pd.read_csv(inflationFile)
    filteredData = [data['Monthly index (month / previous month)'][index]-100 for index in range(59,-1,-1)]
    preparedData = pd.DataFrame(filteredData)
    filepath = Path(data_dir_path + '2.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def unemploymentToCsv():
    global unempFile
    global data_dir_path
    data = pd.read_csv(unempFile)
    filteredData = [data[f"Unemployment rate (in %) 20{year}Q{q}"][0] for year in range(18,23) for q in range(1,5)]
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

# def stockIndexToCsv():
#     global stockIndexFile
#     global data_dir_path
#     data = pd.read_csv(stockIndexFile)
#     filteredData = []
    
#     for year in range(18,23):
#         for month in range(1,13):
#             foundFlag = False
#             start = 0
#             i = 0
#             while (not foundFlag):
#                 if (month >= 10 and data['date'][i].startswith(f"20{year}-{month}")) or (month < 10 and data['date'][i].startswith(f"20{year}-0{month}")):
#                     start = i
#                     foundFlag = True
#                 i += 1
#             foundFlag = False
#             i = start
#             end = 0
#             sum = 0
#             while (not foundFlag):
#                 if (i >= len(data['date'])) or (month >= 10 and data['date'][i].startswith(f"20{year}-{month-1}")) or (month < 10 and data['date'][i].startswith(f"20{year}-0{month-1}")) or (month == 1 and data['date'][i].startswith(f"20{year-1}")):
#                     end = i
#                     foundFlag = True
#                 else:
#                     sum += float(data['change_prev_close_percentage'][i])
#                 i += 1
#             filteredData.append((sum)/(end-start))
#             print(f'Done year 20{year}, month {month}')
#     preparedData = pd.DataFrame(filteredData)
#     filepath = Path(data_dir_path + '5.csv')
#     preparedData.to_csv(filepath, index=False, header=False)

def stockIndexToCsv():
    global stockIndexFile
    global data_dir_path
    data = pd.read_csv(stockIndexFile)
    filteredData = []
    
    for year in range(18,23):
        for month in range(1,13):
            foundFlag = False
            start = 0
            i = len(data['date'])-1
            while (not foundFlag):
                if (month >= 10 and data['date'][i].startswith(f"20{year}-{month}")) or (month < 10 and data['date'][i].startswith(f"20{year}-0{month}")):
                    start = i
                    foundFlag = True
                i -= 1
            foundFlag = False
            i = start
            end = 0
            while (not foundFlag):
                if (i <= 0) or (month >= 9 and data['date'][i].startswith(f"20{year}-{month+1}")) or (month < 9 and data['date'][i].startswith(f"20{year}-0{month+1}")) or (month == 12 and data['date'][i].startswith(f"20{year+1}")):
                    end = i
                    foundFlag = True
                i -= 1
            if not end == 0:
                end += 1
            change = (data["last_value"][end]/data["last_value"][start])*100 - 100
            filteredData.append(change)
            print(f'Done year 20{year}, month {month}: {change}. Start: {data["last_value"][start]}, End: {data["last_value"][end]}')
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
    


