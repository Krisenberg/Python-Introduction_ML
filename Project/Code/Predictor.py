from sklearn.svm import SVR
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple

def predict(SVRModels: Dict[str, Tuple[SVR, StandardScaler]], data_to_predict: List[List[float]],
            output_text_file: str, output_graph_file: str, colors_countries: Dict[str, str]) -> None:
    
    #fig = plt.figure(figsize=(8, 6))
    fig, ax = plt.subplots()
    x_sample_numbers = [i+1 for i in range(len(data_to_predict))]
    for country_name in SVRModels.keys():
        y_pred = SVRModels[country_name][0].predict(SVRModels[country_name][1].transform(data_to_predict))
        print(f'{country_name}: {y_pred}')
        ax.plot(x_sample_numbers, y_pred, colors_countries[country_name], ms = 5)
    ax.set(xlim=(0, len(data_to_predict)+1), ylim=(-20, 20))

    plt.show()
    plt.savefig(output_graph_file)

    