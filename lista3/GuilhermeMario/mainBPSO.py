import math
import numpy as np
import bpso
import plots

# Definir tamanho da população e número de dimensões
population_size = 25
dimensions = 500

# Parâmetros do PSO
inertia = 1
cognitive = 2
social = 2

lista_iteracoes = []
lista_gbest = []
lista_gbest_fitness = []

for i in range(1,31):
    # Executa o PSO binário para resolver o problema OneMax
    best_particle, best_fitness_list, average_fitness_list, worst_fitness_list, itera = bpso.binary_pso(population_size, dimensions, inertia, cognitive, social)

    # Imprime os resultados
    print("Número de iterações:", itera)
    # Imprime os resultados
    print("Best Particle", best_particle)
    print("Best Fitness List", best_fitness_list)
    print("Average Fitness List", average_fitness_list)
    print("Worst Fitness List", worst_fitness_list)
    print("Melhor fitness:", max(best_fitness_list) * dimensions)
    print("Média do fitness:", np.mean(average_fitness_list) * dimensions)
    print("Pior fitness:", min(worst_fitness_list) * dimensions)

    lista_gbest_fitness.append(max(best_fitness_list) * dimensions)
    lista_iteracoes.append(itera)
    lista_gbest.append(best_particle)

    plots.plotFitnessTemporal('BPSO (OneMax D = {}) - execução {}'.format(dimensions, i), list(range(itera)), worst_fitness_list,
                              average_fitness_list, best_fitness_list)

print(lista_iteracoes)
np.savetxt('BPSO (OneMax D = {}) - Lista de iterações', lista_iteracoes, fmt='%d')
np.savetxt('BPSO (OneMax D = {}) - gbests', lista_gbest, fmt='%d')
np.savetxt('BPSO (OneMax D = {}) - gbests_fitness', lista_gbest_fitness, fmt='%d')
plots.plota_boxplot(lista_iteracoes, 'BPSO (OneMax D = {})'.format(dimensions))