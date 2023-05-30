import math
import numpy as np

from bbcso import BBCSO
import plots

dimensoes = 500
#dicionário de parâmetros
parametros = {
    'MR': 0.6,
    'SPM': 5,
    'PMO': 0.4,
    'CDC': math.floor(dimensoes/10)
}

def funcao_fitness(array):
    fitness = np.ndarray.sum(array)
    return fitness

lista_iteracoes = []
lista_gbest = []
lista_gbest_fitness = []

for i in range(1,31):
    bbcso = BBCSO(n_gatos=25, dimensoes=dimensoes, parametros=parametros, funcao_fitness=funcao_fitness)
    iteracoes, melhor_fitness, medio_fitness, pior_fitness = bbcso.run(dimensoes)
    fitness_temp = [melhor_fitness, medio_fitness, pior_fitness]

    valor_maximo = max([max(lista) for lista in fitness_temp]) #Maior fitness de todos
    valor_minimo = min([min(lista) for lista in fitness_temp]) #Menor fitness de todos

    pior_fitness_temporal_nomalizado = [((fit-valor_minimo)/(valor_maximo-valor_minimo)) for fit in fitness_temp[2]]
    medio_fitness_temporal_nomalizado = [((fit-valor_minimo)/(valor_maximo-valor_minimo)) for fit in fitness_temp[1]]
    melhor_fitness_temporal_nomalizado = [((fit-valor_minimo)/(valor_maximo-valor_minimo)) for fit in fitness_temp[0]]

    lista_gbest.append(bbcso.gbest.posicoes)
    lista_gbest_fitness.append(bbcso.gbest_fitness)

    plots.plotFitnessTemporal('BBCSO (OneMax D = {}) - execução {}'.format(dimensoes, i), list(range(iteracoes+1)), pior_fitness_temporal_nomalizado,
                              medio_fitness_temporal_nomalizado, melhor_fitness_temporal_nomalizado)

    lista_iteracoes.append(iteracoes)
print(lista_iteracoes)
np.savetxt('BBCSO (OneMax D = {}) - Lista de iterações'.format(dimensoes), lista_iteracoes, fmt='%d')
np.savetxt('BBCSO (OneMax D = {}) - gbests'.format(dimensoes), lista_gbest, fmt='%d')
np.savetxt('BBCSO (OneMax D = {}) - gbests_fitness'.format(dimensoes), lista_gbest_fitness, fmt='%d')
plots.plota_boxplot(lista_iteracoes, 'BBCSO (OneMax D = {})'.format(dimensoes))