import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Any


def predict(SVRModels: Dict[str, Tuple[Any, float, StandardScaler]],
            data_to_predict: List[List[float]],
            output_graph_file: str, colors_countries: Dict[str, str]) -> None:

    fig, ax = plt.subplots()
    x_sample_numbers = [i+1 for i in range(len(data_to_predict))]
    eurozone_label_set = False
    for country_name in SVRModels.keys():
        y_pred = SVRModels[country_name][0].predict(SVRModels[country_name][2].transform(data_to_predict))
        size = 4
        if country_name == 'Poland':
            size = 7
            ax.plot(x_sample_numbers, y_pred, colors_countries[country_name], label='Poland', ms=size)
        elif not eurozone_label_set:
            ax.plot(x_sample_numbers, y_pred, colors_countries[country_name], label='Eurozone country', ms=size)
            eurozone_label_set = True
        else:
            ax.plot(x_sample_numbers, y_pred, colors_countries[country_name], ms=size)
        ax.errorbar(x_sample_numbers, y_pred, yerr=10, fmt='none', color='black', elinewidth=0.5)
    ax.set(xlim=(0, len(data_to_predict)+1), ylim=(-5, 5))

    # Set the title of the graph
    ax.set_title("Predicted changes of the Stock Index prices for every test scenario")

    # Set titles of the axes
    ax.set_xlabel("Number of test set")
    ax.set_ylabel("Predicted change")

    ax.legend()

    plt.savefig(output_graph_file)
