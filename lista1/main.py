from lista1 import funcoes
from lista1 import plotagem
import numpy as np

x = np.linspace(-500, 500)
y = np.linspace(-500, 500)

x, y = np.meshgrid(x, y)  # Retorna matrizes de cordenadas

z = funcoes.func1(x, y)  # Avalia a função aos longo dos pontos

plotagem.plota_3D(x, y, z, [-500, 500])
