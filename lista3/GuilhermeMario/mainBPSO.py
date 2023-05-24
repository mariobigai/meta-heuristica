import math
import numpy as np
import bpso

# Definir tamanho da população e número de dimensões
population_size = 500
dimensions = 500

# Parâmetros do PSO
inertia = 1
cognitive = 2
social = 2

# Executa o PSO binário para resolver o problema OneMax
best_particle, particle_fitness, best_fitness, itera = bpso.binary_pso(population_size, dimensions, inertia, cognitive, social)

# Imprime os resultados
print("Número de iterações:", itera)
print("Melhor fitness:", best_fitness)
print("Média do fitness:", np.mean(particle_fitness))
print("Pior fitness:", min(particle_fitness))
print("Melhor fitness temporal normalizado:", best_fitness / dimensions)
print("Média do fitness temporal normalizado:", np.mean(particle_fitness) / dimensions)
print("Pior fitness temporal normalizado:", min(particle_fitness) / dimensions)