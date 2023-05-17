import math
import numpy
import numpy as np

from bbcso import BBCSO

dimensoes = 500
#dicionário de parâmetros
parametros = {
    'MR': 0.7,
    'SPM': 5,
    'PMO': 0.4,
    'CDC': math.floor(dimensoes/10)
}

def funcao_fitness(array):
    fitness = np.ndarray.sum(array)
    return fitness

bbcso = BBCSO(n_gatos=500, dimensoes=dimensoes, parametros=parametros, funcao_fitness=funcao_fitness)
iteracoes, melhor_fitness, medio_fitness, pior_fitness = bbcso.run(dimensoes)

fitness_temp = [melhor_fitness, medio_fitness, pior_fitness]

valor_maximo = max([max(lista) for lista in fitness_temp]) #Maior fitness de todos
valor_minimo = min([min(lista) for lista in fitness_temp]) #Menor fitness de todos

pior_fitness_temporal_nomalizado = [((fit-valor_minimo)/(valor_maximo-valor_minimo)) for fit in fitness_temp[2]]
medio_fitness_temporal_nomalizado = [((fit-valor_minimo)/(valor_maximo-valor_minimo)) for fit in fitness_temp[1]]
melhor_fitness_temporal_nomalizado = [((fit-valor_minimo)/(valor_maximo-valor_minimo)) for fit in fitness_temp[0]]

print(bbcso.gbest.posicoes)
print(bbcso.gbest_fitness)
print(iteracoes)
print(melhor_fitness_temporal_nomalizado)
print(melhor_fitness)
print(medio_fitness_temporal_nomalizado)
print(medio_fitness)
print(pior_fitness_temporal_nomalizado)
print(pior_fitness)