import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from typing import Dict, Tuple

def create_model(data_dir_path: str, countryName: str, csv_headers: Dict[int, str],
                 output_text_file: str) -> Tuple[SVR, StandardScaler]:
    filePath = data_dir_path + f"{countryName}\\{countryName}_data.csv"
    data = pd.read_csv(filePath, sep=',')

    file_to_write = open(output_text_file, "a")

    X = data[list(csv_headers.values())[:-1]].values
    y = data[list(csv_headers.values())[-1]].values
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)


    # Scale the input features
    scaler_X = StandardScaler()
    # scaler_y = StandardScaler()
    # scaler_X.fit(X_train)
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)


    # Create and train the SVR model
    svr_model = SVR(kernel='rbf', C=10, gamma='auto')
    svr_model.fit(X_train_scaled, y_train)

    # Make predictions
    #y_pred = svr_model.predict(X_test_scaled)
    #X_test_scaled = scaler_X.transform(X_test)
    y_pred = svr_model.predict(X_test_scaled)
    file_to_write.write('------------------------------------------------------------')
    file_to_write.write(f"Adjusting SVR model for {countryName}")
    file_to_write.write('------------------------------------------------------------\n\n')
    file_to_write.write("First attempt:\n")
    file_to_write.write("Parameters: {'C': 10, 'gamma': 'auto', 'kernel': 'rbf'}\n")
    file_to_write.write("Predicted values vs Real values\n")
    for i in range(len(y_pred)):
        file_to_write.write(f"{y_pred[i]}  {y_test[i]}\n")
    mse_1 = mean_squared_error(y_test, y_pred)
    file_to_write.write(f'Mean squared error for the {countryName} model: {mse_1:0.3}\n\n')
    
    param_grid = {
        'kernel': ['rbf', 'poly'],
        'C': [0.001,0.01,0.5,1,5,10,25,50,100],
        'gamma': ['scale', 'auto']
        #'gamma': [0.001,0.01,1,5]
    }
    grid_search = GridSearchCV(SVR(), param_grid, cv=5, refit=True, scoring='neg_mean_squared_error')
    grid_search.fit(X_train_scaled, y_train)
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_

    # y_pred = best_model.predict(X_test_scaled)
    # y_pred = best_model.predict(X_test_scaled)
    # X_test_scaled = scaler_X.transform(X_test)
    y_pred = grid_search.predict(X_test_scaled)
    file_to_write.write("Second attempt - after Grid Search:\n")
    file_to_write.write(f'Parameters: {best_params}\n')
    file_to_write.write("Predicted values vs Real values\n")
    for i in range(len(y_pred)):
        file_to_write.write(f"{y_pred[i]}  {y_test[i]}\n")
    mse_2 = mean_squared_error(y_test, y_pred)
    file_to_write.write(f'Mean squared error for the {countryName} model: {mse_2:0.3}\n')

    # scores = cross_val_score(svr_model, X_test_scaled, y_test, cv=8, scoring='neg_mean_squared_error')
    # scores = cross_val_score(svr_model, scaler_X.transform(X_test), y_test, cv=8, scoring='neg_mean_squared_error')
    #file_to_write.write(f'Scores: {-scores}\n\n\n')
    file_to_write.close()
    # sns.scatterplot(x=y_test, y=y_pred, alpha=0.6)
    # sns.lineplot(x=y_test, y=y_test)

    # plt.xlabel('Actual value', fontsize=14)
    # plt.ylabel('Predicted value', fontsize=14)
    # plt.show()

    return (best_model, scaler_X)

# def create_model(data_dir_path: str, countryName: str, csv_headers: Dict[int, str],
#                  output_text_file: str) -> SVR:
#     filePath = data_dir_path + f"{countryName}\\{countryName}_data.csv"
#     data = pd.read_csv(filePath, sep=',')

#     file_to_write = open(output_text_file, "a")

#     X = data[list(csv_headers.values())[:-1]].values
#     y = data[list(csv_headers.values())[-1]].values
    
#     # Split the data into training and testing sets
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=50)



#     # Create and train the SVR model
#     svr_model = SVR(kernel='rbf', C=10, gamma='auto')
#     svr_model.fit(X_train, y_train)

#     # Make predictions
#     y_pred = svr_model.predict(X_test)
#     file_to_write.write('------------------------------------------------------------')
#     file_to_write.write(f"Adjusting SVR model for {countryName}")
#     file_to_write.write('------------------------------------------------------------\n\n')
#     file_to_write.write("First attempt:\n")
#     file_to_write.write("Parameters: {'C': 10, 'gamma': 'auto', 'kernel': 'rbf'}\n")
#     file_to_write.write("Predicted values vs Real values\n")
#     for i in range(len(y_pred)):
#         file_to_write.write(f"{y_pred[i]}  {y_test[i]}\n")
#     mse_1 = mean_squared_error(y_test, y_pred)
#     file_to_write.write(f'Mean squared error for the {countryName} model: {mse_1:0.3}\n\n')
    
#     param_grid = {
#         'kernel': ['rbf', 'poly'],
#         'C': [0.001,0.01,0.5,1,5,10,25,50,100],
#         'gamma': ['scale', 'auto']
#         #'gamma': [0.001,0.01,1,5]
#     }
#     grid_search = GridSearchCV(SVR(), param_grid, cv=5, refit=True, scoring='neg_mean_squared_error')
#     grid_search.fit(X_train, y_train)
#     best_model = grid_search.best_estimator_
#     best_params = grid_search.best_params_

#     # y_pred = best_model.predict(X_test_scaled)
#     # y_pred = best_model.predict(X_test_scaled)
#     # X_test_scaled = scaler_X.transform(X_test)
#     y_pred = grid_search.predict(X_test)
#     file_to_write.write("Second attempt - after Grid Search:\n")
#     file_to_write.write(f'Parameters: {best_params}\n')
#     file_to_write.write("Predicted values vs Real values\n")
#     for i in range(len(y_pred)):
#         file_to_write.write(f"{y_pred[i]}  {y_test[i]}\n")
#     mse_2 = mean_squared_error(y_test, y_pred)
#     file_to_write.write(f'Mean squared error for the {countryName} model: {mse_2:0.3}\n')

#     # scores = cross_val_score(svr_model, X_test_scaled, y_test, cv=8, scoring='neg_mean_squared_error')
#     scores = cross_val_score(svr_model, X_test, y_test, cv=8, scoring='neg_mean_squared_error')
#     file_to_write.write(f'Scores: {-scores}\n\n\n')
#     file_to_write.close()

#     return best_model