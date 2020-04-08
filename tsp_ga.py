import random
import numpy as np
import math
import copy
from pyeasyga.pyeasyga import GeneticAlgorithm


def is_repetition(gnm):
    for i in range(len(gnm)):
        for j in range(i + 1, len(gnm)):
            if gnm[i] == gnm[j]:
                return True
    return False

def generate_adj_mat(N):
    adj_mat = np.random.randint(0, 50, (N, N))
    for i in range(adj_mat.shape[1]):
        adj_mat[i, i] = 0
        for j in range(i + 1, adj_mat.shape[1]):
            adj_mat[j, i] = adj_mat[i, j]

    for _ in range(5):
        i = np.random.randint(N)
        j = np.random.randint(N)
        if i != j:
            adj_mat[i, j] = 0
            adj_mat[j, i] = 0
    return adj_mat

N = 10

adj_mat = generate_adj_mat(N)

print("Szombszédsági mátrix:")
print(adj_mat)

ga = GeneticAlgorithm(list(range(N)), 500, 200)

def create_individual(data):
    return np.random.randint(0, N, len(data))

ga.create_individual = create_individual

def crossover(parent1, parent2):
    c_idx = random.randrange(1, parent1.shape[0])
    child_1 = np.append(parent1[:c_idx], parent2[c_idx:])
    child_2 = np.append(parent2[:c_idx], parent1[c_idx:])
    return child_1, child_2

ga.crossover_function = crossover

def mutate(individual):
    m_idx = random.randrange(individual.shape[0])
    x = random.randrange(0, N)
    while x == individual[m_idx]:
        x = random.randrange(0, N)
    individual[m_idx] = x

ga.mutate_function = mutate

def fitness(individual, data):
    f = 0
    if is_repetition(individual):
        return -math.inf
    else:
        for i in range(individual.shape[0]):
            if i == individual.shape[0] - 1:
                if adj_mat[individual[i]][individual[0]] == 0:
                    return -math.inf
                else:
                    f += adj_mat[individual[i]][individual[0]]
                    break
            if adj_mat[individual[i]][individual[i + 1]] == 0:
                return -math.inf
            else:
                f -= adj_mat[individual[i]][individual[i + 1]]
    return f

ga.fitness_function = fitness
ga.run()

best = ga.best_individual()

print("Optimális út:")
print(best[1])
print("Út hossza: ", -best[0])


        