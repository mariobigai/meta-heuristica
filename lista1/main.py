from lista1 import funcoes
from lista1 import plotagem
import numpy as np
from lista1 import AlgoritmoGenetico

## Define os limites e cria o linspace
x = np.arange(-5, 5, 0.05)
y = np.arange(-5, 5, 0.05)

X = np.meshgrid(x, y)  # Retorna matrizes de cordenadas

z = funcoes.func2(X)  # Avalia a função aos longo dos pontos

modelo, solucao = AlgoritmoGenetico.ga_lib(funcoes.func2, 2, np.array([[-5, 5]]*2),
                                           150, 0, 50, 0.99, 1, 0.5)

best_ponto = [solucao[0], solucao[1], funcoes.func2(solucao)]
plotagem.plota_3D(X[0], X[1], z, best_ponto) #Plota o gráfico
