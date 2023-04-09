#"""
import math
import numpy as np
from lista1 import funcoes
#"""
import numpy as np
from geneticalgorithm2 import geneticalgorithm2 as ga
from geneticalgorithm2 import AlgorithmParams
from geneticalgorithm2 import Crossover
from geneticalgorithm2 import plot_several_lines

"""
Iremos varias os modelos de AG com duas propostas de crossover e duas de seleção combinadas aos pares:

Crossovers: Mixed, e Aritimético
Seleção: Torneio e Roleta
"""
# Crossover:uniforme  Seleção:Roleta
parametros_uniforme_roleta=AlgorithmParams(
                     max_num_iteration = 200,
                     population_size = 150,
                     mutation_probability = 0.03,
                     mutation_discrete_probability = None,
                     elit_ratio = 0,
                     parents_portion = 0.2,
                     crossover_type = 'uniform',
                     mutation_type = 'uniform_by_center',
                     selection_type = 'roulette',
                     max_iteration_without_improv = 15
                     )
# Crossover:uniforme Seleção:torneio
parametros_uniforme_torneio=AlgorithmParams(
                     max_num_iteration = 200,
                     population_size = 150,
                     mutation_probability = 0.03,
                     mutation_discrete_probability = None,
                     elit_ratio = 0,
                     parents_portion = 0.2,
                     crossover_type = 'uniform',
                     mutation_type = 'uniform_by_center',
                     selection_type = 'tournament',
                     max_iteration_without_improv = 15
                     )

#Crossover: Aritmético Seleção:Roleta
parametros_aritmetico_roleta=AlgorithmParams(
                     max_num_iteration = 200,
                     population_size = 150,
                     mutation_probability = 0.03,
                     mutation_discrete_probability = None,
                     elit_ratio = 0,
                     parents_portion = 0.2,
                     crossover_type = Crossover.arithmetic(),
                     mutation_type = 'uniform_by_center',
                     selection_type = 'roulette',
                     max_iteration_without_improv = 15
                     )

#Crossover: Aritmético Seleção:Torneio
parametros_aritmetico_torneio=AlgorithmParams(
                     max_num_iteration = 200,
                     population_size = 150,
                     mutation_probability = 0.03,
                     mutation_discrete_probability = None,
                     elit_ratio = 0,
                     parents_portion = 0.2,
                     crossover_type = Crossover.arithmetic(),
                     mutation_type = 'uniform_by_center',
                     selection_type = 'tournament',
                     max_iteration_without_improv = 15
                     )

lista_parametros = [parametros_uniforme_roleta, parametros_uniforme_torneio, parametros_aritmetico_roleta, parametros_aritmetico_torneio]
def retorna_modelo(limites, parametros, funcao):
    modelo = ga(funcao, dimension = 2,
                    variable_type='real',
                     variable_boundaries = limites,
                     #function_timeout = 15,
                     algorithm_parameters=parametros
                )
    return modelo

def gera_modelos(limites, funcao, lista = lista_parametros):
    return [retorna_modelo(limites, par, funcao) for par in lista]


if (__name__ == "__main__"):
    modelo = retorna_modelo(np.array([[-5,5]]*2), lista_parametros[-1], funcoes.func2)
    modelo.checked_reports.extend(
        [('report_avarage', np.mean), ('report_worst', np.max)]
    )
    print(str(modelo.crossover))
    print(str(modelo.selection))

    melhor_modelo = 0
    melhor_fitness_geral = math.inf
    lista_num_gen = []

    modelo.run(no_plot=True)
    solucao = modelo.result
    print('\n')
    print(funcoes.func2(solucao.variable))
    # for _ in range(10):
    #     modelo.run(no_plot=True)
    #     num_geracoes = len(modelo.report)
    #     lista_num_gen.append(num_geracoes)
    #     melhor_fitness = modelo.result.score
    #     if melhor_fitness < melhor_fitness_geral:
    #         melhor_fitness_geral = melhor_fitness
    #         melhor_modelo = modelo
    #
    # names = [name for name, _ in melhor_modelo.checked_reports[::-1]]
    # plot_several_lines(
    #     lines=[getattr(melhor_modelo, name) for name in names],
    #     colors=('green', 'red', 'blue'),
    #     labels=['pior fitness', 'fitness medio', 'melhor fitness'],
    #     linewidths=(1, 1.5, 1, 2),
    # )

    # print(lista_num_gen)
