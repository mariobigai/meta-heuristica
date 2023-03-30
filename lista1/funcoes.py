import numpy as np

def func1(x, y):
    # Função de Schwefel com d = 2
    return 418.9829 * 2 - x * np.sin(np.sqrt(abs(x))) - y * np.sin(np.sqrt(abs(y)))

def func2(x, y):
    # Função de Rastrigin
    return 20 + x**2 + y**2 - 10*(np.cos(2*np.pi*x) + np.cos(2*np.pi*y))

def func3(x, y):
    # Função Exponencial
    return x * np.exp(-(x**2 + y**2))
