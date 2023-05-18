import random
import time

class Particle:
    def __init__(self, num_dimensions):
        self.position = [random.randint(0, 1) for _ in range(num_dimensions)]
        self.velocity = [0] * num_dimensions
        self.best_position = self.position.copy()

    def update_velocity(self, global_best_position, inertia_weight, cognitive_weight, social_weight):
        for i in range(len(self.velocity)):
            cognitive_component = cognitive_weight * random.random() * (self.best_position[i] - self.position[i])
            social_component = social_weight * random.random() * (global_best_position[i] - self.position[i])
            self.velocity[i] = inertia_weight * self.velocity[i] + cognitive_component + social_component

    def update_position(self):
        for i in range(len(self.position)):
            if random.random() < sigmoid(self.velocity[i]):
                self.position[i] = 1
            else:
                self.position[i] = 0

    def evaluate_fitness(self):
        return sum(self.position)

def sigmoid(x):
    return 1 / (1 + pow(2.71828, -x))

def calculate_normalized_fitness(fitness, max_fitness):
    return fitness / max_fitness

def one_max_pso(num_particles, num_dimensions):
    particles = [Particle(num_dimensions) for _ in range(num_particles)]
    global_best_fitness = float('-inf')
    global_best_position = particles[0].best_position.copy()

    fitness_values = []
    start_time = time.time()

    iteration = 0
    while global_best_fitness < num_particles:
        iteration_best_fitness = float('-inf')
        iteration_total_fitness = 0

        for particle in particles:
            fitness = particle.evaluate_fitness()
            if fitness > global_best_fitness:
                particle.best_position = particle.position.copy()
                global_best_fitness = fitness
                global_best_position = particle.position.copy()

            iteration_best_fitness = max(iteration_best_fitness, fitness)
            iteration_total_fitness += fitness

        fitness_values.append(iteration_best_fitness)

        for particle in particles:
            particle.update_velocity(global_best_position, 1, 2, 2)  # Aumentando a velocidade
            particle.update_position()

        iteration += 1
        print(global_best_fitness)

    end_time = time.time()

    best_fitness = max(fitness_values)
    average_fitness = sum(fitness_values) / len(fitness_values)
    worst_fitness = min(fitness_values)

    normalized_best_fitness = calculate_normalized_fitness(best_fitness, num_dimensions)
    normalized_average_fitness = calculate_normalized_fitness(average_fitness, num_dimensions)
    normalized_worst_fitness = calculate_normalized_fitness(worst_fitness, num_dimensions)

    execution_time = end_time - start_time

    return global_best_position, best_fitness, average_fitness, worst_fitness, normalized_best_fitness, normalized_average_fitness, normalized_worst_fitness, execution_time

# Exemplo de uso
num_particles = 100
num_dimensions = 100

solution, best_fitness, average_fitness, worst_fitness, normalized_best_fitness, normalized_average_fitness, normalized_worst_fitness, execution_time = one_max_pso(num_particles, num_dimensions)
print("Melhor solução encontrada:", solution)
print("Melhor fitness:", best_fitness)
print("Média fitness:", average_fitness)
print("Pior fitness:", worst_fitness)
print("Melhor fitness temporal normalizado:", normalized_best_fitness)
print("Média fitness temporal normalizado:", normalized_average_fitness)
print("Pior fitness temporal normalizado:", normalized_worst_fitness)
print("Tempo de execução:", execution_time, "segundos")
