import random
from typing import List, Tuple

def generate_population(size: int, letters: List[str]) -> List[dict]:
    population = []
    attempts = 0

    while len(population) < size and attempts < size * 10:
        individual = {}
        values = random.sample(range(10), len(letters))
        for letter, value in zip(letters, values):
            individual[letter] = value

        if len(set(individual.values())) == len(individual.values()):  # Ensure all values are unique
            population.append(individual)
        attempts += 1

    if len(population) < size:
        raise ValueError("Failed to generate a diverse initial population.")
    
    return population

def decode(individual: dict, word: str) -> int:
    return int(''.join(str(individual[letter]) for letter in word))

def fitness(individual: dict, word1: str, word2: str, word3: str) -> int:
    # Ensure all letters have unique values
    if len(set(individual.values())) != len(individual.values()):
        return float('inf')  # Penalize solutions with duplicate values
    
    # Ensure first letters are not zero
    if individual[word1[0]] == 0 or individual[word2[0]] == 0 or individual[word3[0]] == 0:
        return float('inf')  # Penalize solutions where the first letter is zero

    # Ensure last_value1+last_value2=last_value3
    last_entity = individual[word1[-1]] + individual[word2[-1]]
    if last_entity > 10:
        if last_entity - 10 != individual[word3[-1]]:
            return float('inf')
        
    if last_entity < 10 and last_entity != individual[word3[-1]]:
        return float('inf')  # Penalize solutions where the first letter is zero

    # voltar a string
    val1 = decode(individual, word1)
    val2 = decode(individual, word2)
    val3 = decode(individual, word3)
    # print(val1, '+', val2, '-', val3, 'result:', val1 + val2 - val3)
    return abs((val1 + val2) - val3)

def mutate(individual: dict, letters: List[str]) -> dict:
    mutated = individual.copy()
    letter = random.choice(letters)
    new_value = random.choice([i for i in range(10) if i not in individual.values()])
    mutated[letter] = new_value
    return mutated

def crossover(parent1: dict, parent2: dict) -> dict:
    child = {}
    for key in parent1.keys():
        child[key] = parent1[key] if random.random() > 0.5 else parent2[key]

    if len(set(child.values())) != len(child.values()):
        return mutate(child, list(child.keys()))  # Mutate if duplicate values are introduced
    return child

def genetic_algorithm(word1: str, word2: str, word3: str, population_size: int = 300, generations: int = 3000):
    letters = list(set(word1 + word2 + word3))
    if len(letters) > 10:
        raise ValueError("Maximum of 10 unique letters allowed.")

    population = generate_population(population_size, letters)
    stagnation_counter = 0
    last_best_fitness = float('inf')

    print(generations)
    for generation in range(generations):
        population.sort(key=lambda ind: fitness(ind, word1, word2, word3))
        best_fitness = fitness(population[0], word1, word2, word3)
        print('best: ', best_fitness)
        if best_fitness == 0:
            print(f"Solution found in generation {generation}")
            return population[0]

        # Check for stagnation
        if best_fitness == last_best_fitness:
            stagnation_counter += 1
        else:
            stagnation_counter = 0
            last_best_fitness = best_fitness

        if stagnation_counter >= 500:
            print("Population stagnated. Regenerating new individuals.")
            print(len(population))
            new_individuals = generate_population(population_size // 2, letters)
            new_individuals.sort(key=lambda ind: fitness(ind, word1, word2, word3))
            population = population[:population_size // 2] + new_individuals
            population.sort(key=lambda ind: fitness(ind, word1, word2, word3))
            stagnation_counter = 0
            print(len(population))

        next_generation = population[:20]  # Elitism: carry over the top 20

        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(population[:-1], 2)
            child = crossover(parent1, parent2)
            rand = random.random()
            if rand < 0.15:  # 15% mutation rate
                child = mutate(child, letters)
            next_generation.append(child)

        population = next_generation

        if generation % 100 == 0:
            print(f"Generation {generation}, Best Fitness: {best_fitness}")

    print("No solution found.")
    return None

if __name__ == "__main__":
    # Example input
    word1 = input("Enter the first word: ").upper()
    word2 = input("Enter the second word: ").upper()
    word3 = input("Enter the result word: ").upper()

    solution = genetic_algorithm(word1, word2, word3)
    if solution:
        print("Solution:", solution)
        print(f"{word1} + {word2} = {word3}")
        print(f"{decode(solution, word1)} + {decode(solution, word2)} = {decode(solution, word3)}")
