"""
Task: implement LSS method.

Here are some useful hints:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.lstsq.html
# https://www.statsoft.pl/textbook/stathome_stat.html?https%3A%2F%2Fwww.statsoft.pl%2Ftextbook%2Fstglm.html
"""
import urllib.request
import os
from typing import Tuple
from numpy.linalg import inv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def fetch_data_file() -> str:
    """Download a file with target data to fit LSS algo in."""
    file = "GDP_happiness.csv"
    url_server = "https://byes.pl/wp-content/uploads/datasets/" + file
    if not os.path.isfile(file):
        urllib.request.urlretrieve(url_server, file)
    else:
        print(f"File already exists!")
    return file


def read_data_vectors() -> Tuple[np.ndarray, np.ndarray]:
    """Read target data and obtain X and Y vectors without NaNs."""
    gdp_happines_df = pd.read_csv(fetch_data_file(), index_col=[0])
    gdp_happines_df = gdp_happines_df.fillna(gdp_happines_df.mean(axis=0))
    gdp_happines_df.tail()

    X = gdp_happines_df["GDP per capita"].values
    Y = gdp_happines_df["happiness"].values

    return X, Y


def get_polynomial_form(polynomial_degree: int) -> np.ndarray:
    """
    Get array with form of polynomial.

    :param polynomial_degree: a degree of polynomial
        [[0], [1]] - 1st order, [[0], [1], [2]] - 2nd order, 
        [[0], [1], [2], [3]] - 3rd order, and so on...
    :return: an array with degrees of polynomial
    """
    array = np.arange(polynomial_degree+1)
    result_array=array.reshape((-1,1))
    return result_array


def print_polynomial(theta: np.ndarray, precission: int = 3) -> str:
    """Return string representation of polynomial."""
    str_polynomial = ""
    for index, coeff in np.ndenumerate(theta):
        str_polynomial += str(np.round(coeff,precission)) + "*x^" + str(index[0])
        if (index[0] < len(theta)-1):
            str_polynomial += " + "
    return str_polynomial


def least_squares_solution(
        X: np.ndarray, Y: np.ndarray, polynomial_degree: int
) -> np.ndarray:
    """
    Compute theta matrix with coefficients of polynomial fitted by LSS.

    :param X: argument vector, shape = (N, )
    :param Y: target vector, shape = (N, ) 
    :param polynomial_degree: degree of fitted polynomial

    :return: theta matrix of polynomial, shape = (1, polynomial_degree + 1)
    """
    """First attempt"""
    # N = len(X)
    # X_mat = np.empty(shape=((polynomial_degree+1), N), dtype=float)
    # for degree in range(0, (polynomial_degree+1)):
    #     for x in range(0, N):
    #         X_mat[degree][x] = (X[x]**degree)
    # coeff = (inv((X_mat @ (X_mat.T))) @ X_mat) @ Y.T
    # result_theta = coeff.reshape(-1,1)
    # return result_theta
    """Second attempt - refactored formula, using get_polynomial"""
    polynomial_array = get_polynomial_form(polynomial_degree)
    X_mat = np.array([np.power(X,degree) for degree in polynomial_array])
    theta = (inv((X_mat @ (X_mat.T))) @ X_mat) @ (Y.T)
    result_theta = theta.reshape(-1,1)
    return result_theta


def generalised_linear_model(X: np.ndarray, T: np.ndarray) -> np.ndarray:
    """
    Compute values for generalised linear model.

    :param X: argument vector, shape = (N, )
    :param T: theta matrix of polynomial, shape = (1, polynomial_degree + 1)
    :return: regressed values, shape = (N, )
    """
    return sum([coeff * X ** degree for degree, coeff in enumerate(T)])


def visualise_LSS_method(X: np.ndarray, Y: np.ndarray, T: np.ndarray):
    """
    Visualise LSS model on fancy Matplotlib plot.

    :param X: input argument vector
    :param Y: input target vector
    :param T: theta vector with coefficients of ploynomial
    """
    X_test = np.linspace(start=X.min(), stop=X.max(), num=300)
    Y_pred = generalised_linear_model(X_test, T)
    plt.scatter(X, Y, color="tab:blue", label="real data")
    plt.plot(X_test, Y_pred, color="tab:orange", label="estimated function")
    plt.xlabel("x - GDP", fontsize=14)
    plt.ylabel("y - happiness", fontsize=14)
    plt.title(f"Fitted: \n {print_polynomial(T, precission=5)}")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # here is a playground for your tests!
    X, Y = read_data_vectors()
    T = least_squares_solution(X, Y, 7)
    print(print_polynomial(T))
    visualise_LSS_method(X, Y, T)
