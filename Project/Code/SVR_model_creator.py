import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

data_dir_path = "C:\\Users\\Kris\\Documents\\Studia\\Semestr_IV\\MSiD_L\\Project\\Data\\"
countries_set = {
    "Portugal",
    "Slovenia"
}

def plot5Dchart(data, countryName):
    # Visualizing 5-D mix data using bubble charts
    fig = plt.figure(figsize=(8, 6))
    fig.subplots_adjust(left=0.01, right=0.9, bottom=0.05, top=0.95)
    ax = fig.add_subplot(111, projection='3d')
    t = fig.suptitle(f'Stock Index change vs macroeconomic factors - {countryName}', fontsize=12)

    xs = [float(data['Inflation change (%)'][i]) for i in range(len(data['Inflation change (%)']))]
    ys = [float(data['GDP change (%)'][i]) for i in range(len(data['GDP change (%)']))]
    zs = [float(data['Stock Index change (%)'][i]) for i in range(len(data['Stock Index change (%)']))]
    data_points = [(x, y, z) for x, y, z in zip(xs, ys, zs)]

    min_interest_rate = min(data['Interest rates change (%)'])
    sizes = []
    if min_interest_rate < 0:
        sizes = [float((data['Interest rates change (%)'][i]+abs(min_interest_rate)+0.01))*500 for i in range(len(data['Interest rates change (%)']))]
    else:
        sizes = [float(data['Interest rates change (%)'][i])*500 for i in range(len(data['Interest rates change (%)']))]
    colors = [float(data['Unemployment change (%)'][i]) for i in range(len(data['Unemployment change (%)']))]

    cmap = plt.colormaps.get_cmap('viridis')
    sc = ax.scatter(xs, ys, zs, c=colors, cmap=cmap, alpha=0.4, edgecolors='none', s=sizes)

    cbar = plt.colorbar(sc)
    cax = cbar.ax
    cax_pos = cax.get_position()
    cax.set_position([cax_pos.x0+0.1, cax_pos.y0+0.1, cax_pos.width * 0.6, cax_pos.height * 0.6])


    ax.set_xlabel('Inflation change (%)')
    ax.set_ylabel('GDP change (%)')
    ax.set_zlabel('Stock Index change (%)')
    cbar.set_label('Unemployment change (%)')

    plt.savefig(data_dir_path + f"General\\{countryName}_graph.png")

def plotHistogram(data, countryName):
    data.hist(bins=5, color='steelblue', edgecolor='black', linewidth=1.0,
           xlabelsize=8, ylabelsize=8, grid=False)    
    plt.tight_layout()
    histFile = data_dir_path + f"General\\{countryName}_hist.png"
    plt.savefig(histFile)

def create_model(countryName):
    filePath = data_dir_path + f"{countryName}\\{countryName}_data.csv"
    data = pd.read_csv(filePath, sep=',')
    plotHistogram(data, countryName)
    plot5Dchart(data, countryName)
    X = data[['GDP change (%)', 'Inflation change (%)', 'Unemployment change (%)', 'Interest rates change (%)']].values
    y = data['Stock Index change (%)'].values
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    # Scale the input features
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Create and train the SVR model
    svr_model = SVR(kernel='rbf', C=50, gamma='auto')
    svr_model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = svr_model.predict(X_test_scaled)
    print('------------------------------------------------------------')
    print(f"Adjusting SVR model for {countryName}")
    print('------------------------------------------------------------', end='\n\n')
    print("First attempt:")
    print(f"Predicted values: {y_pred}")
    print(f"Real values: {y_test}")
    MSE_SVR = mean_squared_error(y_test, y_pred)
    print(f'Mean squared error for the {countryName} model: {MSE_SVR:0.3}', end='\n\n')
    
    param_grid = {
        'kernel': ['rbf', 'poly'],
        'C': [0.001,0.009,0.01,0.09,1,5,10,25,50,100],
        'gamma': ['scale', 'auto']
    }
    grid_search = GridSearchCV(svr_model, param_grid, cv=5, scoring='neg_mean_squared_error')
    grid_search.fit(X_test_scaled, y_test)
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_

    y_pred = best_model.predict(X_test_scaled)
    print("Second attempt - after Grid Search:")
    print(f"Predicted values: {y_pred}")
    print(f"Real values: {y_test}")
    MSE_SVR = mean_squared_error(y_test, y_pred)
    print(f'Mean squared error for the {countryName} model: {MSE_SVR:0.3}')
    print(f'Parameters: {best_params}')

    scores = cross_val_score(svr_model, X_test_scaled, y_test, cv=8, scoring='neg_mean_squared_error')
    print(f'Scores: {-scores}', end='\n\n')
    return best_model

if __name__ == "__main__":
    create_model("Portugal")
    # create_model("Slovenia")
    # create_model("Spain")
    # create_model("Greece")
    # create_model("Latvia")