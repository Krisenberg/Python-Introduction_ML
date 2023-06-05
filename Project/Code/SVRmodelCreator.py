import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from typing import Dict, Tuple, List, Any, Optional
from numpy import ndarray

def createSVRmodel(X_train_scaled: ndarray, X_test_scaled: ndarray,
                     y_train: ndarray, y_test: ndarray, 
                     countryName: str, output_text_file: str) -> Optional[Tuple[SVR, float]]:
    
    file_to_write = open(output_text_file, "a")
    # Create and train the SVR model
    svr_model = SVR(kernel='rbf', C=10, gamma='auto')
    svr_model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = svr_model.predict(X_test_scaled)
    file_to_write.write('------------------------------------------------------------')
    file_to_write.write(f"Adjusting SVR model for {countryName}")
    file_to_write.write('------------------------------------------------------------\n\n')
    file_to_write.write("First attempt:\n")
    file_to_write.write("Parameters: {'C': 10, 'gamma': 'auto', 'kernel': 'rbf'}\n")
    file_to_write.write("Predicted values vs Real values\n")
    for i in range(len(y_pred)):
        file_to_write.write(f"{y_pred[i]}  {y_test[i]}\n")
    mse = mean_squared_error(y_test, y_pred)
    file_to_write.write(f'Mean squared error for the {countryName} model: {mse:0.3}\n\n')
    file_to_write.close()
    if np.allclose(y_pred, y_pred[0], atol=0.15):
        return None
    return (svr_model, mse)


def createRFRmodel(X_train_scaled: ndarray, X_test_scaled: ndarray,
                     y_train: ndarray, y_test: ndarray, 
                     countryName: str, output_text_file: str) -> Optional[Tuple[RandomForestRegressor, float]]:
    
    file_to_write = open(output_text_file, "a")
    # Create and train the SVR model
    rfr_model = RandomForestRegressor(n_estimators=10, max_features='sqrt', max_depth=3)
    rfr_model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = rfr_model.predict(X_test_scaled)
    file_to_write.write('------------------------------------------------------------')
    file_to_write.write(f"Adjusting RFR model for {countryName}")
    file_to_write.write('------------------------------------------------------------\n\n')
    file_to_write.write("First attempt:\n")
    file_to_write.write("Parameters: {'n_estimators': 10, 'max_features': 'sqrt', 'max_depth': '3'}\n")
    file_to_write.write("Predicted values vs Real values\n")
    for i in range(len(y_pred)):
        file_to_write.write(f"{y_pred[i]}  {y_test[i]}\n")
    mse = mean_squared_error(y_test, y_pred)
    file_to_write.write(f'Mean squared error for the {countryName} model: {mse:0.3}\n\n')
    file_to_write.close()
    if np.allclose(y_pred, y_pred[0], atol=0.15):
        return None
    return (rfr_model, mse)


def createGridSearch(X_train_scaled: ndarray, X_test_scaled: ndarray,
                     y_train: ndarray, y_test: ndarray, model: Any,
                     param_grid: Dict[str, List[Any]],
                     countryName: str, output_text_file: str) -> Optional[Tuple[GridSearchCV, float]]:
    
    file_to_write = open(output_text_file, "a")

    scoring = ['neg_mean_squared_error']
    grid_search = GridSearchCV(model, param_grid=param_grid, cv=None, refit='neg_mean_squared_error', scoring=scoring)
    grid_results = grid_search.fit(X_train_scaled, y_train)
    best_model = grid_results.best_estimator_
    best_params = grid_results.best_params_

    # y_pred = grid_search.predict(X_test_scaled)
    y_pred = best_model.predict(X_test_scaled)
    file_to_write.write("Second attempt - after Grid Search:\n")
    file_to_write.write(f'Parameters: {best_params}\n')
    file_to_write.write("Predicted values vs Real values\n")
    for i in range(len(y_pred)):
        file_to_write.write(f"{y_pred[i]}  {y_test[i]}\n")
    mse = mean_squared_error(y_test, y_pred)
    file_to_write.write(f'Mean squared error for the {countryName} model: {mse:0.3}\n')
    file_to_write.close()
    if np.allclose(y_pred, y_pred[0], atol=0.15):
        return None
    return (best_model, mse)


def create_model(data_dir_path: str, countryName: str, csv_headers: Dict[int, str],
                 output_text_file: str) -> Tuple[Any, float, StandardScaler]:
    
    filePath = data_dir_path + f"{countryName}\\{countryName}_data.csv"
    data = pd.read_csv(filePath, sep=',')

    file_to_write = open(output_text_file, "a")

    X = data[list(csv_headers.values())[:-1]].values
    y = data[list(csv_headers.values())[-1]].values
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)


    # Scale the input features
    scaler_X = StandardScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)

    # # Create and train the SVR model
    # svr_model = SVR(kernel='rbf', C=10, gamma='auto')
    # svr_model.fit(X_train_scaled, y_train)

    # # Make predictions
    # y_pred = svr_model.predict(X_test_scaled)
    # file_to_write.write('------------------------------------------------------------')
    # file_to_write.write(f"Adjusting SVR model for {countryName}")
    # file_to_write.write('------------------------------------------------------------\n\n')
    # file_to_write.write("First attempt:\n")
    # file_to_write.write("Parameters: {'C': 10, 'gamma': 'auto', 'kernel': 'rbf'}\n")
    # file_to_write.write("Predicted values vs Real values\n")
    # for i in range(len(y_pred)):
    #     file_to_write.write(f"{y_pred[i]}  {y_test[i]}\n")
    # mse_1 = mean_squared_error(y_test, y_pred)
    # file_to_write.write(f'Mean squared error for the {countryName} model: {mse_1:0.3}\n\n')
    models_results = {}
    svr = createSVRmodel(X_train_scaled, X_test_scaled, y_train, y_test, countryName, output_text_file)
    if svr is not None:
        models_results[svr[0]]=svr[1]
    
    param_grid = {
        'kernel': ['rbf', 'poly'],
        'C': [0.001,0.01,0.5,1,5,10,25,50,100],
        'gamma': ['scale', 'auto']
    }
    # scoring = ['neg_mean_squared_error']
    # new_model = SVR(gamma='auto')
    # grid_search = GridSearchCV(new_model, param_grid=param_grid, cv=None, refit='neg_mean_squared_error', scoring=scoring)
    # grid_results = grid_search.fit(X_train_scaled, y_train)
    # best_model = grid_results.best_estimator_
    # best_params = grid_results.best_params_

    # # y_pred = grid_search.predict(X_test_scaled)
    # y_pred = best_model.predict(X_test_scaled)
    # file_to_write.write("Second attempt - after Grid Search:\n")
    # file_to_write.write(f'Parameters: {best_params}\n')
    # file_to_write.write("Predicted values vs Real values\n")
    # for i in range(len(y_pred)):
    #     file_to_write.write(f"{y_pred[i]}  {y_test[i]}\n")
    # mse_2 = mean_squared_error(y_test, y_pred)
    # file_to_write.write(f'Mean squared error for the {countryName} model: {mse_2:0.3}\n')

    # scores = cross_val_score(svr_model, X_test_scaled, y_test, cv=8, scoring='neg_mean_squared_error')
    # scores = cross_val_score(svr_model, scaler_X.transform(X_test), y_test, cv=8, scoring='neg_mean_squared_error')
    #file_to_write.write(f'Scores: {-scores}\n\n\n')
    svr_gs = createGridSearch(X_train_scaled, X_test_scaled, y_train, y_test, SVR(),
                              param_grid, countryName, output_text_file)
    if svr_gs is not None:
        models_results[svr_gs[0]]=svr_gs[1]

    rfr = createRFRmodel(X_train_scaled, X_test_scaled, y_train, y_test, countryName, output_text_file)
    if rfr is not None:
        models_results[rfr[0]]=rfr[1]
    
    param_grid = {
        'n_estimators': [10,20,30],
        'max_features': ['sqrt'],
        'max_depth': [2,3,5] 
    }
    rfr_gs = createGridSearch(X_train_scaled, X_test_scaled, y_train, y_test, RandomForestRegressor(),
                              param_grid, countryName, output_text_file)
    if rfr_gs is not None:
        models_results[rfr_gs[0]]=rfr_gs[1]
    
    min_pair = min(models_results.items(), key=lambda x: x[1])

    return (min_pair[0], min_pair[1], scaler_X)

# def create_model(data_dir_path: str, countryName: str, csv_headers: Dict[int, str],
#                  output_text_file: str) -> Tuple[SVR, StandardScaler]:
    
#     filePath = data_dir_path + f"{countryName}\\{countryName}_data.csv"
#     data = pd.read_csv(filePath, sep=',')

#     file_to_write = open(output_text_file, "a")

#     X = data[list(csv_headers.values())[:-1]].values
#     y = data[list(csv_headers.values())[-1]].values
    
#     # Split the data into training and testing sets
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

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
#     }
#     scoring = ['neg_mean_squared_error']
#     new_model = SVR(gamma='auto')
#     grid_search = GridSearchCV(new_model, param_grid=param_grid, cv=None, refit='neg_mean_squared_error', scoring=scoring)
#     grid_results = grid_search.fit(X_train, y_train)
#     best_model = grid_results.best_estimator_
#     best_params = grid_results.best_params_

#     # y_pred = grid_search.predict(X_test_scaled)
#     y_pred = best_model.predict(X_test)
#     file_to_write.write("Second attempt - after Grid Search:\n")
#     file_to_write.write(f'Parameters: {best_params}\n')
#     file_to_write.write("Predicted values vs Real values\n")
#     for i in range(len(y_pred)):
#         file_to_write.write(f"{y_pred[i]}  {y_test[i]}\n")
#     mse_2 = mean_squared_error(y_test, y_pred)
#     file_to_write.write(f'Mean squared error for the {countryName} model: {mse_2:0.3}\n')

#     # scores = cross_val_score(svr_model, X_test_scaled, y_test, cv=8, scoring='neg_mean_squared_error')
#     # scores = cross_val_score(svr_model, scaler_X.transform(X_test), y_test, cv=8, scoring='neg_mean_squared_error')
#     #file_to_write.write(f'Scores: {-scores}\n\n\n')
#     file_to_write.close()

#     return (best_model, StandardScaler())
