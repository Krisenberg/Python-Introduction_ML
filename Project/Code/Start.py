import os
import DataPreprocessing
import ChartsCreator

# !!!!!!!!!!!!!! IMPORTANT !!!!!!!!!!!!!! #
# Please set a valid path to the directory, where all data has been downloaded
path_to_data_dir = "C:\\Users\\Kris\\Documents\\Studia\\Semestr_IV\\MSiD_L\\Project\\Data\\"
# --------------------------------------- #

os.environ['DATA_PATH'] = path_to_data_dir

dir_for_charts = 'Charts\\'

data_files_names = {
    1: 'GDP.csv',
    2: 'Inflation.csv',
    3: 'Unemployment.csv',
    4: 'InterestRates.csv',
    5: 'StockIndex.csv'
}

data_features_functions = {
    1: DataPreprocessing.GDPToCsv,
    2: DataPreprocessing.inflationToCsv,
    3: DataPreprocessing.unemploymentToCsv,
    4: DataPreprocessing.interestRatesToCsv,
}

new_csv_headers = {
    1: 'GDP change (%)',
    2: 'Inflation change (pp)',
    3: 'Unemployment change (pp)',
    4: 'Interest rates change (pp)',
    5: 'Stock Index change (%)'
}

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


def prepareAllData() -> bool:
    flag = True

    for country_name in stock_prices_filters.keys():
        result = DataPreprocessing.prepareData(country_name, data_files_names, data_features_functions,
                                               stock_prices_filters[country_name], new_csv_headers)
        print(result[1])
        if not result[0]:
            flag = False

    if flag:
        print("\nData is ready.")
    else:
        print("\nData needs to be fixed.")

    return flag


def visualiseData() -> None:
    data_dir_path = (os.environ.get('DATA_PATH')) if os.environ.get('DATA_PATH', '') != '' else None

    # check if DATA_PATH is set correctly
    if data_dir_path is not None:
        chars_directory = data_dir_path+dir_for_charts
        if not os.path.isdir(chars_directory):
            os.mkdir(chars_directory)
        for country_name in stock_prices_filters.keys():
            ChartsCreator.plot5Dchart(data_dir_path, country_name, dir_for_charts, new_csv_headers)
            ChartsCreator.plotHistogram(data_dir_path, country_name, dir_for_charts)


def run() -> None:
    data_state = prepareAllData()
    if not data_state:
        print('Program terminates. Data is not prepared for the further analysis.')

    visualiseData()
    print('Data has been visualised. All the charts are available in the directory specified above.')


if __name__ == '__main__':
    run()
