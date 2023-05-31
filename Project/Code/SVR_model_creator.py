import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

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