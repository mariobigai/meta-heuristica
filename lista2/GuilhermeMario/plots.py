import seaborn as sns
import operator
import matplotlib.pyplot as plt

def plotMapa(nome_cidade, cities, path: list, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()

    x = []
    y = []
    for point in cities:
        x.append(point[1])
        y.append(point[2])
    y = list(map(operator.sub, [max(y) for i in range(len(cities))], y))
    ax.plot(x, y, 'c.', alpha=0.5)

    for _ in range(1, len(path)):
        i = path[_ - 1]
        j = path[_]
        ax.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True, width=0.001)

    i = path[-1]
    j = path[0]
    ax.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True, width=0.001)

    ax.set_xlim(min(x) - 50, max(x) + 50)
    ax.set_ylim(min(y) / 1.1, max(y) * 1.1)

    fig.savefig(f'{nome_cidade}.png')
    return ax


def plota_boxplot(dados, nome_cidade, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()
    
    sns.boxplot(data=dados, ax=ax)
    ax.set_title(f'{nome_cidade}')
    ax.set_ylabel("Gerações")
    
    fig.savefig(f'./Boxplot{nome_cidade}.png')
    
    return ax

def plotFitnessTemporal(titulo, gen, fitPior, fitMedio, fitMelhor, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()
    
    fig.suptitle(titulo)
    ax.plot(gen, fitPior, label="Pior fitness")
    ax.plot(gen, fitMedio, label="Fitness médio")
    ax.plot(gen, fitMelhor, label="Melhor fitness")
    ax.legend()
    ax.set_xlabel("Gerações")
    ax.set_ylabel("Fitness Normalizado")
    
    fig.savefig(f'./Temporal {titulo}.png')
    
    return ax