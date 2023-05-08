import seaborn as sns
import operator
import matplotlib.pyplot as plt

#points é os pontos no mapa da cidade
def plotMapa(nome_cidade, cities, path: list):
       x = []
       y = []
       for point in cities:
              x.append(point[1])
              y.append(point[2])
       # noinspection PyUnusedLocal
       y = list(map(operator.sub, [max(y) for i in range(len(cities))], y))
       plt.plot(x, y, 'co')

       for _ in range(1, len(path)):
              i = path[_ - 1]
              j = path[_]
              # noinspection PyUnresolvedReferences
              plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)

       # Conecta o ultimo ponto ao primeiro
       i = path[-1]
       j = path[0]
       # noinspection PyUnresolvedReferences
       plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)

       # noinspection PyTypeChecker
       plt.xlim(min(x) / 1.01, max(x) * 1.01)
       # noinspection PyTypeChecker
       plt.ylim(min(y) / 1.1, max(y) * 1.1)
       # Salva o plot como um arquivo PNG
       plt.savefig(f'{nome_cidade}.png')
       plt.show()


def plota_boxplot(dados, nome_cidade):
       #Coleta os dados para o boxplot
       sns.boxplot(data= dados)
       #Insere um titulo
       plt.title(f'{nome_cidade}')
       #Insere o nome para o eixo y
       plt.ylabel("Gerações")
       #Salva o boxplot
       plt.savefig(f'./Boxplot{nome_cidade}')
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

