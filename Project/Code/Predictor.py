from sklearn.svm import SVR
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Any

def predict(SVRModels: Dict[str, Tuple[Any, float, StandardScaler]], data_to_predict: List[List[float]],
            output_graph_file: str, colors_countries: Dict[str, str]) -> None:
    
    #fig = plt.figure(figsize=(8, 6))
    fig, ax = plt.subplots()
    x_sample_numbers = [i+1 for i in range(len(data_to_predict))]
    for country_name in SVRModels.keys():
        y_pred = SVRModels[country_name][0].predict(SVRModels[country_name][2].transform(data_to_predict))
        print(f'{country_name}: {y_pred}')
        size = 4
        if country_name=='Poland':
            size=7
        ax.plot(x_sample_numbers, y_pred, colors_countries[country_name], ms = size)
        #ax.errorbar(x_sample_numbers, y_pred, yerr = np.sqrt(SVRModels[country_name][1]))
        #plt.errorbar(x_sample_numbers, y_pred, yerr = np.sqrt(SVRModels[country_name][1]))
        ax.errorbar(x_sample_numbers, y_pred, yerr=10, fmt='none', color='black',elinewidth=0.5)
    ax.set(xlim=(0, len(data_to_predict)+1), ylim=(-5, 5))

    # Set title of the graph
    ax.set_title("Predicted changes of the Stock Index prices for every test set of parameters")
    
    # Set titles of the axes
    ax.set_xlabel("Number of test set")
    ax.set_ylabel("Predicted change")

    ax.legend()

    plt.savefig(output_graph_file)
    plt.show()

    