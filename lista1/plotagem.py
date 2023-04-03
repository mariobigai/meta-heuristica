# Arquivo destinado a aos códigos para plotagem das funções no R3

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator

def plota_3D(X, Y, Z, limits):
       #Cria figura e eixos
       fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

       # Plota a superfície
       surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                              linewidth=0, antialiased=False)

       # Customização do eixo z.
       #ax.set_zlim(limits[0], limits[1])
       ax.zaxis.set_major_locator(LinearLocator(10))

       # A StrMethodFormatter is used automatically
       ax.zaxis.set_major_formatter('{x:.02f}')

       plt.show()