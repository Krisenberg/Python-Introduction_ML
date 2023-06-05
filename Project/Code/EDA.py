# from pandas_profiling import ProfileReport
import ydata_profiling as pdp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# def firstAttempt(data_dir_path:str, country_name:str) -> None:
#     data_path = data_dir_path + country_name + f'\\{country_name}_data.csv'
#     data = pd.read_csv(data_path)
#     sns.pairplot(data, hue="Stock Index change (%)")
#     plt.show()

#     corrmat = data.corr()
#     hm = sns.heatmap(corrmat,
#                      cbar=True,
#                      annot=True,
#                      square=True,
#                      fmt='.2f',
#                      annot_kws={'size': 10},
#                      yticklabels=data.columns,
#                      xticklabels=data.columns,
#                      cmap="Spectral_r")
#     plt.show()


def exploratoryDataAnalysis(data_dir_path: str, country_name: str,
                            eda_dir: str) -> None:
    data_path = data_dir_path + country_name + f'\\{country_name}_data.csv'
    data = pd.read_csv(data_path)
    report = pdp.ProfileReport(data)
    report_path = data_dir_path + eda_dir + f'{country_name}_eda.html'
    report.to_file(report_path)


def generalEDA(data_dir_path: str, general_dir: str, eda_dir: str) -> None:
    data_path = data_dir_path + general_dir + 'general_data.csv'
    data = pd.read_csv(data_path)
    report = pdp.ProfileReport(data)
    report_path = data_dir_path + eda_dir + 'general_eda.html'
    report.to_file(report_path)
