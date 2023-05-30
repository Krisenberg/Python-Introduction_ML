from pathlib import Path
import os
from typing import Tuple, Dict, Callable, List
import pandas as pd
import numpy as np
from datetime import datetime

def dataExists(data_dir_path: str, expected_file_names: set[str]) -> Tuple[bool, str]:
    """
    Function used for checking, if all needed data exists in the directory specified by DATA_PATH
    """
    actual_files_names: set[str] = {entry.name for entry in os.scandir(data_dir_path)}
    for file_name in expected_file_names:
        if not f'{file_name}.csv' in actual_files_names:
            return (False, f"File {file_name} is missing!")
    return (True, "All files are present")


def GDPToCsv(data_dir_path: str) -> None:
    """
    Function which filters the values of the GDP change in every quarter and computes the change in
    every month. Then all the computed values are being saved to the temporary file to be merged later.
    """
    data = pd.read_csv(data_dir_path + "GDP.csv")
    start = data['TIME'].values.tolist().index('2018-Q1')
    stop = data['TIME'].values.tolist().index('2022-Q4')
    step = 1 if stop >= start else -1
    stop_index = stop + 1 if stop >= start else stop - 1
    filteredData = [data['Value'][i] for i in range (start, stop_index, step)]
    preparedData = pd.DataFrame([(100 * np.cbrt((100 + float(filteredData[i]))/100))-100 for i in range(len(filteredData)) for _ in range(3)])
    filepath = Path(data_dir_path + '1.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def inflationToCsv(data_dir_path: str) -> None:
    """
    Function which filters the values of the Inflation in every month (100% -> year 2015) 
    and computes the change in every month. Then all the computed values are being saved 
    to the temporary file to be merged later.
    """
    data = pd.read_csv(data_dir_path + "Inflation.csv")
    start = data['TIME'].values.tolist().index('2017-12')
    stop = data['TIME'].values.tolist().index('2022-12')
    step = 1 if stop >= start else -1
    stop_index = stop + 1 if stop >= start else stop - 1
    filteredData = [data['Value'][i] for i in range (start, stop_index, step)]
    preparedData = pd.DataFrame([(100 * (filteredData[i]/filteredData[i-1]))-100 for i in range(1, len(filteredData))])
    filepath = Path(data_dir_path + '2.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def unemploymentToCsv(data_dir_path: str) -> None:
    """
    Function which filters the values of the Unemployment rate in every month 
    and computes the change from the prevoius month. Then all the computed values are being saved 
    to the temporary file to be merged later.
    """
    data = pd.read_csv(data_dir_path + "Unemployment.csv")
    start = data['TIME'].values.tolist().index('2017-12')
    stop = data['TIME'].values.tolist().index('2022-12')
    step = 1 if stop >= start else -1
    stop_index = stop + 1 if stop >= start else stop - 1
    filteredData = [data['Value'][i] for i in range(start, stop_index, step)]
    preparedData = pd.DataFrame([(100 * (filteredData[i]/filteredData[i-1]))-100 for i in range(1, len(filteredData))])
    filepath = Path(data_dir_path + '3.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def interestRatesToCsv(data_dir_path: str) -> None:
    """
    Function which filters the values of the Interest rates in every month 
    and computes the change from the prevoius month. Then all the computed values are being saved 
    to the temporary file to be merged later.
    """
    data = pd.read_csv(data_dir_path + "InterestRates.csv")    
    start = data['date'].values.tolist().index('2017-12-31')
    stop = data['date'].values.tolist().index('2022-12-31')
    step = 1 if stop >= start else -1
    stop_index = stop + 1 if stop >= start else stop - 1
    filteredData = [data['s1'][i] if not data['s1'][i]==0 else 0.009 for i in range(start, stop_index, step)]
    # recalculatedData = [(100 * (filteredData[i]/filteredData[i-1]))-100 for i in range(1, len(filteredData))]
    # preparedData = pd.DataFrame([recalculatedData[i] if abs(recalculatedData[i])<=100 else recalculatedData[i]//100 for i in range(len(recalculatedData))])
    recalculatedData = [filteredData[i] - filteredData[i-1] for i in range(1, len(filteredData))]
    preparedData = pd.DataFrame(recalculatedData)
    filepath = Path(data_dir_path + '4.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def greeceStockIndex(data_dir_path: str) -> None:
    data = pd.read_csv(data_dir_path + "StockIndex.csv") 
    computedData = []
    stock_dates = data['Date'].values.tolist()
    index = len(stock_dates)-1
    
    for year in range(18,23):
        for month in range(1,13):
            first = index
            while(index > 0 and not (datetime.strptime(stock_dates[index-1],"%m/%d/%y").year > datetime.strptime(stock_dates[index],"%m/%d/%y").year or datetime.strptime(stock_dates[index-1],"%m/%d/%y").month > datetime.strptime(stock_dates[index],"%m/%d/%y").month)):
                index -= 1
            last = index
            change = (data[" Close"][last]/data[" Open"][first])*100 - 100
            computedData.append(change)
            index -= 1

    preparedData = pd.DataFrame(computedData)
    filepath = Path(data_dir_path + '5.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def latviaStockIndex(data_dir_path: str) -> None:
    data = pd.read_csv(data_dir_path + "StockIndex.csv") 
    computedData = []
    stock_dates = data['Date'].values.tolist()
    index = len(stock_dates)-1
    
    for year in range(18,23):
        for month in range(1,13):
            first = index
            while(index > 0 and not (datetime.strptime(stock_dates[index-1],"%m/%d/%Y").year > datetime.strptime(stock_dates[index],"%m/%d/%Y").year or datetime.strptime(stock_dates[index-1],"%m/%d/%Y").month > datetime.strptime(stock_dates[index],"%m/%d/%Y").month)):
                index -= 1
            last = index
            close_price_str = data["Price"][last].replace(',', '')
            open_price_str = data["Open"][first].replace(',', '')
            change = (float(close_price_str)/float(open_price_str))*100 - 100
            computedData.append(change)
            index -= 1

    preparedData = pd.DataFrame(computedData)
    filepath = Path(data_dir_path + '5.csv')
    preparedData.to_csv(filepath, index=False, header=False)

def mergeData(data_dir_path: str, country_name: str, headers: List[str]) -> None:
    """
    Function that merges all prepared data from files: 1,2,3,4,5. It creates a csv file that is used
    later in the data analysis.
    """
    merged_df = pd.DataFrame()
    for i in range(1,6):
        file_path = data_dir_path + (f"{i}.csv")
        temp_df = pd.read_csv(file_path, header=None)
        merged_df = pd.concat([merged_df, temp_df], axis=1)

    mergedFile = Path(data_dir_path + f'{country_name}_data.csv')
    merged_df.to_csv(mergedFile, index=False, header=headers)

def prepareData(country_name: str, expected_file_names: set[str],
                stock_prices_filters: Dict[str, Callable], new_csv_headers: List[str]) -> Tuple[bool, str]:
    data_dir_path = (os.environ.get('DATA_PATH')) if os.environ.get('DATA_PATH', '') != '' else None

    #check if DATA_PATH is set correctly
    if data_dir_path is not None:
        data_dir_path += (country_name+"\\")
        data_existence = dataExists(data_dir_path, expected_file_names)
        #check if all neded data is available
        if not data_existence[0]:
            return data_existence

        GDPToCsv(data_dir_path)
        inflationToCsv(data_dir_path)
        unemploymentToCsv(data_dir_path)
        interestRatesToCsv(data_dir_path)
        # call the function that filters stock index data from that country
        stock_prices_filters[country_name](data_dir_path)
        mergeData(data_dir_path, country_name, new_csv_headers)
        return (True, f'Data has been succesfully preprocessed for: {country_name}')

    else:
        return (False, 'DATA_PATH variable is not set')

    