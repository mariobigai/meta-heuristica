import seaborn as sns
import matplotlib.pyplot as plt

def plota_boxplot(dados, algoritmo, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()
    
    sns.boxplot(data=dados, ax=ax)
    ax.set_title(f'Box-plot {algoritmo}')
    ax.set_ylabel("Iterações")
    
    fig.savefig(f'./Boxplot{algoritmo}.png')
    
    return ax

def plotFitnessTemporal(titulo, iter, fitPior, fitMedio, fitMelhor, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()
    
    fig.suptitle(titulo)
    ax.plot(iter, fitPior, label="Pior fitness")
    ax.plot(iter, fitMedio, label="Fitness médio")
    ax.plot(iter, fitMelhor, label="Melhor fitness")
    ax.legend()
    ax.set_xlabel("Iterações")
    ax.set_ylabel("Fitness Normalizado")
    
    fig.savefig(f'./Temporal {titulo}.png')
    
    return ax