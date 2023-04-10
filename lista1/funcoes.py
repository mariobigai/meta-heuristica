import numpy as np

## func(X) , onde X será um numpy.ndarray

def func1(X):
    # Função de Schwefel com d = 2
    return 418.9829 * 2 - X[0] * np.sin(np.sqrt(abs(X[0]))) - X[1] * np.sin(np.sqrt(abs(X[1])))

def func2(X):
    # Função de Rastrigin
    return 20 + X[0]**2 + X[1]**2 - 10*(np.cos(2*np.pi*X[0]) + np.cos(2*np.pi*X[1]))

def func3(X):
    # Função Exponencial R3
    return (X[0] * np.exp(-(X[0]**2 + X[1]**2)))
def func4(X):
    # fitness para função exponencial Função Exponencial
    return 1/(1+(X[0] * np.exp(-(X[0]**2 + X[1]**2))))
