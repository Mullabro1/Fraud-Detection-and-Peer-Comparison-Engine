import pandas as pd
import numpy as np
import random

# Sample financial dataset
data = {
    'Current_Ratio': [1.8, 0.9, 1.2, 2.1, 0.7, 1.5, 0.8, 1.3, 1.7, 0.7],
    'Debt_to_Equity': [0.8, 2.0, 1.4, 0.6, 2.5, 1.3, 2.1, 1.6, 0.9, 3.0],
    'OCF_to_Debt': [0.25, 0.10, 0.15, 0.30, 0.05, 0.18, 0.08, 0.12, 0.27, 0.03],
    'ROA': [0.08, 0.03, 0.05, 0.09, 0.01, 0.06, 0.02, 0.04, 0.07, -0.02],
    'Financial_Health': ['Healthy', 'Critical', 'At Risk', 'Healthy', 'Critical', 'At Risk', 'Critical', 'At Risk', 'Healthy', 'Critical']
}

df = pd.DataFrame(data)
X = df.drop(columns=['Financial_Health']).values
y = df['Financial_Health'].values

# Genetic Algorithm Parameters
POP_SIZE = 20  # Population size
GENES = X.shape[1]  # Number of features
MUTATION_RATE = 0.1
GENERATIONS = 50

def fitness(individual):
    """Fitness function: Measures how well a set of weights classifies the data."""
    scores = np.dot(X, individual)  # Weighted sum
    predictions = ['Healthy' if score > np.median(scores) else 'Critical' for score in scores]
    return np.sum(predictions == y)  # Count correct classifications

def create_individual():
    """Create a random individual (set of weights)."""
    return np.random.uniform(-1, 1, GENES)

def mutate(individual):
    """Mutate an individual by slightly modifying one gene."""
    if random.random() < MUTATION_RATE:
        idx = random.randint(0, GENES - 1)
        individual[idx] += np.random.uniform(-0.5, 0.5)
    return individual

def crossover(parent1, parent2):
    """Crossover two parents to create a child."""
    point = random.randint(1, GENES - 1)
    return np.concatenate((parent1[:point], parent2[point:]))

# Initialize Population
population = [create_individual() for _ in range(POP_SIZE)]

# Run Genetic Algorithm
for generation in range(GENERATIONS):
    population = sorted(population, key=fitness, reverse=True)  # Sort by fitness
    new_population = population[:POP_SIZE // 2]  # Keep the top half
    while len(new_population) < POP_SIZE:
        p1, p2 = random.sample(new_population, 2)
        child = crossover(p1, p2)
        child = mutate(child)
        new_population.append(child)
    population = new_population

# Best solution
best_weights = population[0]
print("Best weights found:", best_weights)

# Test dataset
test_data = np.array([
    [1.5, 1.0, 0.2, 0.06],
    [0.8, 2.2, 0.1, 0.02],
    [2.0, 0.7, 0.3, 0.09],
    [1.1, 1.5, 0.15, 0.04],
    [0.6, 3.0, 0.05, 0.01]
])

test_scores = np.dot(test_data, best_weights)
threshold = np.median(np.dot(X, best_weights))

predictions = ["Healthy" if score > threshold else "Critical" for score in test_scores]

print("Test Data Predictions:", predictions)