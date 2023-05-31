import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import numpy as np
import seaborn as sns
from typing import Dict

def plot5Dchart(data_dir_path: str, countryName: str, dir_for_charts: str, new_csv_headers: Dict[int, str]):
    filePath = data_dir_path + f"{countryName}\\{countryName}_data.csv"
    data = pd.read_csv(filePath, sep=',')
    # Visualizing 5-D mix data using bubble charts
    fig = plt.figure(figsize=(8, 6))
    fig.subplots_adjust(left=0.01, right=0.9, bottom=0.05, top=0.95)
    ax = fig.add_subplot(111, projection='3d')
    t = fig.suptitle(f'Stock Index change vs macroeconomic factors - {countryName}', fontsize=12)

    xs = [float(data[new_csv_headers[1]][i]) for i in range(len(data[new_csv_headers[1]]))]
    ys = [float(data[new_csv_headers[2]][i]) for i in range(len(data[new_csv_headers[2]]))]
    zs = [float(data[new_csv_headers[5]][i]) for i in range(len(data[new_csv_headers[5]]))]
    #data_points = [(x, y, z) for x, y, z in zip(xs, ys, zs)]

    min_interest_rate = min(data[new_csv_headers[4]])
    sizes = []
    if min_interest_rate < 0:
        sizes = [float((data[new_csv_headers[4]][i]+abs(min_interest_rate)+0.01))*500 for i in range(len(data[new_csv_headers[4]]))]
    else:
        sizes = [float(data[new_csv_headers[4]][i])*500 for i in range(len(data[new_csv_headers[4]]))]
    colors = [float(data[new_csv_headers[3]][i]) for i in range(len(data[new_csv_headers[3]]))]

    cmap = plt.colormaps.get_cmap('viridis')
    sc = ax.scatter(xs, ys, zs, c=colors, cmap=cmap, alpha=0.4, edgecolors='none', s=sizes)

    cbar = plt.colorbar(sc)
    cax = cbar.ax
    cax_pos = cax.get_position()
    cax.set_position([cax_pos.x0+0.1, cax_pos.y0+0.1, cax_pos.width * 0.6, cax_pos.height * 0.6])


    ax.set_xlabel(new_csv_headers[1])
    ax.set_ylabel(new_csv_headers[2])
    ax.set_zlabel(new_csv_headers[5])
    cbar.set_label(new_csv_headers[3])

    plt.savefig(data_dir_path + f"{dir_for_charts}{countryName}_graph.png")

def plotHistogram(data_dir_path: str, countryName: str, dir_for_charts: str):
    filePath = data_dir_path + f"{countryName}\\{countryName}_data.csv"
    data = pd.read_csv(filePath, sep=',')
    data.hist(bins=8, color='steelblue', edgecolor='black', linewidth=1.0,
           xlabelsize=8, ylabelsize=8, grid=False)    
    plt.tight_layout()
    histFile = data_dir_path + f"{dir_for_charts}{countryName}_hist.png"
    plt.savefig(histFile)