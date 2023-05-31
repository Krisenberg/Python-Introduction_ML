import os
import DataPreprocessing

# !!!!!!!!!!!!!! IMPORTANT !!!!!!!!!!!!!! #
# Please set a valid path to the directory, where all data has been downloaded
path_to_data_dir = "C:\\Users\\Kris\\Documents\\Studia\\Semestr_IV\\MSiD_L\\Project\\Data\\"
# --------------------------------------- #

os.environ['DATA_PATH'] = path_to_data_dir

data_files_names = {
    'GDP',
    'Inflation',
    'Unemployment',
    'InterestRates',
    'StockIndex'
}

new_csv_headers = [
    'GDP change (%)', 
    'Inflation change (%)', 
    'Unemployment change (%)', 
    'Interest rates change (%)', 
    'Stock Index change (%)'
]

"""
This is a dictionary which assigns the proper function to the country. That function
does a data preprocessing on Stock Market Data, since for each country this data may be
downloaded in a different format.
Every other data used in this project has a common source:

- all values of GDP change come from:
https://data.oecd.org/gdp/quarterly-gdp.htm?fbclid=IwAR1hZ_lkQwxmsCFggAmZbSV48rVFww_rHpHDB3PJ8QYB-VcGLTHy0ivdBrE

- all values of Inflation change come from:
https://data.oecd.org/price/inflation-cpi.htm?fbclid=IwAR3WuAsEid4XBH5QMGcya2gLFx6EyGkgHWymOKO-DudbMWte4jOCv4NiQfs

- all values of Unemployment rate come from:
https://data.oecd.org/unemp/unemployment-rate.htm?fbclid=IwAR23Dcu1jN52UBTrjPVQWpFLRU8Dno01TnhS5En8VTRMq7IXeBcPt-lWE1s

- all values of Interest Rates come from one website:
https://sdw.ecb.europa.eu

The easiest way to find them is to type: '<country name>, Long-term interest rate for convergence purposes'
and choose the link from the mentioned website.
"""
stock_prices_filters = {
    'Poland': DataPreprocessing.wsjAPIStockIndex,
    'Greece': DataPreprocessing.wsjAPIStockIndex,
    'Latvia': DataPreprocessing.investingAPIStockIndex,
    'Portugal': DataPreprocessing.investingAPIStockIndex,
    'Lithuania': DataPreprocessing.investingAPIStockIndex,
    'Slovakia': DataPreprocessing.investingAPIStockIndex,
    'Spain': DataPreprocessing.investingAPIStockIndex,
    'Slovenia': DataPreprocessing.ljseAPIStockIndex
}

def prepareAllData():
    for country_name in stock_prices_filters.keys():
        result = DataPreprocessing.prepareData(country_name, data_files_names, stock_prices_filters, new_csv_headers)
        print(result[1])
    # result = DataPreprocessing.prepareData('Greece', data_files_names, stock_prices_filters, new_csv_headers)
    # print(result[1])
    # result = DataPreprocessing.prepareData('Latvia', data_files_names, stock_prices_filters, new_csv_headers)
    # print(result[1])
    # result = DataPreprocessing.prepareData('Portugal', data_files_names, stock_prices_filters, new_csv_headers)
    # print(result[1])
    # result = DataPreprocessing.prepareData('Poland', data_files_names, stock_prices_filters, new_csv_headers)
    # print(result[1])
    # result = DataPreprocessing.prepareData('Slovenia', data_files_names, stock_prices_filters, new_csv_headers)
    # print(result[1])

if __name__ == '__main__':
    prepareAllData()