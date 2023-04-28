# Arquivo destinado a aos códigos para plotagem das funções no R3

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import seaborn as sns

def gera_x_y(lista_np_arrays):
       x, y, b = [], [], []
       for i in range(len(lista_np_arrays)):
              ai = lista_np_arrays[i]
              x.append(ai[0])
              y.append(ai[1])
       b.append(x)
       b.append(y)
       return b

def plota_3D(X, Y, Z, func=None, todas_solus=None, melhores_solus=None, melhor_solu_de_todas=None):
       #Cria figura e eixos
       fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

       # Customização do eixo z.
       #ax.set_zlim(limits[0], limits[1])
       ax.zaxis.set_major_locator(LinearLocator(10))

       # A StrMethodFormatter is used automatically
       ax.zaxis.set_major_formatter('{x:.02f}')

       if func is not None:
              for i in range(len(todas_solus)):
                     ax.scatter(todas_solus[i][0], todas_solus[i][1], func(todas_solus[i]), c='red', marker='.', s=30)
              for i in range(len(melhores_solus)):
                     ax.scatter(melhores_solus[i][0], melhores_solus[i][1], func(melhores_solus[i]), c='black', marker='x', s=40)
              ax.scatter(melhor_solu_de_todas[0], melhor_solu_de_todas[1], func(melhor_solu_de_todas), c='purple', marker='o', s=60)

       # Plota a superfície
       ax.plot_surface(X, Y, Z, cmap=cm.jet, alpha=0.65)
       plt.show()

def plota_boxplot(dados, modelo_nome, nome_func):
       #Coleta os dados para o boxplot
       sns.boxplot(data= dados)
       #Insere um titulo
       plt.title(f'{modelo_nome} {nome_func}')
       #Insere o nome para o eixo y
       plt.ylabel("Gerações")
       #Salva o boxplot
       plt.savefig(f'./Boxplot{modelo_nome}{nome_func}')
       #Plota o boxplot
       plt.show()

def plotFitnessTemporal(titulo, gen, fitPior, fitMedio, fitMelhor):
       fig, ax = plt.subplots()
       fig.suptitle(titulo)
       ax.plot(gen, fitPior, label="Pior fitness")
       ax.plot(gen, fitMedio, label="Fitness médio")
       ax.plot(gen, fitMelhor, label="Melhor fitness")
       plt.legend()
       ax.set_xlabel("Gerações")
       ax.set_ylabel("Fitness Normalizado")
       plt.savefig(f'./Temporal {titulo}')
       plt.show()
