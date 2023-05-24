import random
import numpy as np

# Função de avaliação (fitness)
def evaluate_particle(particle):
    return sum(particle)

# Função de inicialização da população
def initialize_population(pop_size, num_dimensions):
    population = []
    for _ in range(pop_size):
        particle = [random.randint(0, 1) for _ in range(num_dimensions)]
        population.append(particle)
    return population

# Atualiza a melhor posição global
def update_global_best(population, global_best, global_best_fitness):
    for particle in population:
        fitness = evaluate_particle(particle)
        if fitness > global_best_fitness:
            global_best = particle
            global_best_fitness = fitness
    return global_best, global_best_fitness

# Atualiza a velocidade e posição da partícula
def update_particle(particle, velocity, personal_best, global_best, inertia_weight, cognitive_weight, social_weight):
    new_velocity = []
    new_particle = []
    for i in range(len(particle)):
        inertia_term = inertia_weight * velocity[i]
        cognitive_term = cognitive_weight * random.uniform(0, 1) * (personal_best[i] - particle[i])
        social_term = social_weight * random.uniform(0, 1) * (global_best[i] - particle[i])
        new_velocity.append(inertia_term + cognitive_term + social_term)
        new_particle.append(1 if random.uniform(0, 1) < sigmoid(new_velocity[i]) else 0)
    return new_particle, new_velocity

# Função sigmoid para atualizar a posição binária da partícula
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Algoritmo PSO binário
def binary_pso(pop_size, num_dimensions, i_w, c_w, s_w):
    inertia_weight = i_w
    cognitive_weight = c_w
    social_weight = s_w

    population = initialize_population(pop_size, num_dimensions)
    velocity = [[random.uniform(-1, 1) for _ in range(num_dimensions)] for _ in range(pop_size)]
    personal_best = population.copy()
    personal_best_fitness = [evaluate_particle(particle) for particle in population]

    global_best_fitness = max(personal_best_fitness)
    global_best_index = personal_best_fitness.index(global_best_fitness)
    global_best = personal_best[global_best_index]

    iteration = 0
    while global_best_fitness < num_dimensions:
        for i in range(pop_size):
            particle, velocity[i] = update_particle(
                population[i], velocity[i], personal_best[i], global_best, inertia_weight, cognitive_weight, social_weight
            )
            population[i] = particle

            fitness = evaluate_particle(particle)
            if fitness > personal_best_fitness[i]:
                personal_best[i] = particle
                personal_best_fitness[i] = fitness

        global_best, global_best_fitness = update_global_best(population, global_best, global_best_fitness)

        iteration += 1
        print(global_best_fitness)

    return global_best, personal_best_fitness, global_best_fitness, iteration
