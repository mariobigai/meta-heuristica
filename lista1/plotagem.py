# Arquivo destinado a aos códigos para plotagem das funções no R3

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import seaborn as sns

def plota_3D(X, Y, Z, best_ponto=None):
       #Cria figura e eixos
       fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

       # Plota a superfície
       ax.plot_surface(X, Y, Z, cmap=cm.jet,
                              linewidth=0, antialiased=False)

       # Customização do eixo z.
       #ax.set_zlim(limits[0], limits[1])
       ax.zaxis.set_major_locator(LinearLocator(10))

       # A StrMethodFormatter is used automatically
       ax.zaxis.set_major_formatter('{x:.02f}')

       if best_ponto is not None:
              ax.scatter(best_ponto[0], best_ponto[1], best_ponto[2], c='black', marker='o', s=40)

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
