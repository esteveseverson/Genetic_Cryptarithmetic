# low quality population gen, but faster generation

import os
import random
from typing import List


def generate_population(
    size: int,
    letters: List[str],
    word1: str,
    word2: str,
    word3: str,
) -> List[dict]:
    population = []

    while len(population) < size:
        individual = {}
        values = random.sample(range(10), len(letters))
        for letter, value in zip(letters, values):
            individual[letter] = value

        # Ensure all values are unique
        if len(set(individual.values())) == len(individual.values()):
            if fitness(individual, word1, word2, word3) < 8500:
                population.append(individual)
        # print(len(population))

    if len(population) < size:
        raise ValueError("Failed to generate a diverse initial population.")

    return population


def decode(individual: dict, word: str) -> int:
    return int(''.join(str(individual[letter]) for letter in word))


def fitness(individual: dict, word1: str, word2: str, word3: str) -> float:
    # Ensure all letters have unique values
    if len(set(individual.values())) != len(individual.values()):
        # print('not unique values')
        return float('inf')

    # Ensure first letters are not zero
    if (
        (individual[word1[0]] == 0) or (individual[word2[0]] == 0) or (individual[word3[0]] == 0)
    ):
        # print('number starts with 0')
        return float('inf')

    # Validate last and penultimate sums
    last_entity_sum = individual[word1[-1]] + individual[word2[-1]]
    penult_entity_sum = individual[word1[-2]] + individual[word2[-2]]

    # Check carry-over for last digit
    if last_entity_sum >= 10:
        if (last_entity_sum - 10) != individual[word3[-1]]:
            # print('last entity problem1')
            return float('inf')
        # Check carry-over for penultimate digit
        if (penult_entity_sum + 1) % 10 != individual[word3[-2]]:
            # print('penult entity problem')
            return float('inf')
    else:
        if last_entity_sum != individual[word3[-1]]:
            # print('last entity problem2')
            return float('inf')
        if penult_entity_sum % 10 != individual[word3[-2]]:
            # print('penult entity problem')
            return float('inf')

    # print('all validations check')

    # Decode and calculate fitness
    val1 = decode(individual, word1)
    val2 = decode(individual, word2)
    val3 = decode(individual, word3)
    return abs((val1 + val2) - val3) / 100


def mutate(individual: dict, letters: List[str], word1: str, word2: str, word3: str) -> dict:
    mutated = individual.copy()
    letter = random.choice(letters)
    new_value = random.randint(1, 9)
    
    # if exists, change between
    if new_value in individual.values():
        for k, v in individual.items():
            if v == new_value:
                mutated[k], mutated[letter] = mutated[letter], mutated[k]
                break
    else:
        mutated[letter] = new_value
    
    if fitness(mutated, word1, word2, word3) < fitness(individual, word1, word2, word3):
        return individual
    
    return mutated


def crossover(parent1: dict, parent2: dict, word1, word2, word3) -> dict:
    child = {}
    for key in parent1.keys():
        child[key] = parent1[key] if random.random() > 0.5 else parent2[key]

    if len(set(child.values())) != len(child.values()):
        # Assert the mutate dont duplicate a individual
        return mutate(child, list(child.keys()), word1, word2, word3)
    return child


def genetic_algorithm(
    word1: str,
    word2: str,
    word3: str,
    population_size: int = 100,
    generations: int = 3000,
):
    letters = list(set(word1 + word2 + word3))
    if len(letters) > 10:
        raise ValueError("Maximum of 10 unique letters allowed.")

    population = generate_population(
        population_size,
        letters,
        word1,
        word2,
        word3
    )
    stagnation_counter = 0
    reset_counter = 0
    best_fitness = float('inf')
    last_best_fitness = float('inf')

    for generation in range(generations):
        population.sort(key=lambda ind: fitness(ind, word1, word2, word3))
        best_fitness = fitness(population[0], word1, word2, word3)

        if best_fitness == 0:
            print(f"\n\nSolution found with {best_fitness} fitness,", end=' ')
            print(f'in generation {generation}')
            return population[0]

        # Check for stagnation
        if best_fitness == last_best_fitness:
            stagnation_counter += 1
        else:
            stagnation_counter = 0
            last_best_fitness = best_fitness

        if stagnation_counter >= 50:
            if reset_counter < 5:
                keep_size = population_size * 0.1
                new_individuals = generate_population(
                    keep_size,
                    letters,
                    word1,
                    word2,
                    word3
                )
                population = population[:int(keep_size)] + new_individuals
                population.sort(
                    key=lambda ind: fitness(ind, word1, word2, word3)
                )
                stagnation_counter = 0
            else:
                print('-' * 20)
                print("Population stagnated several times, kill generation")
                population = generate_population(
                    population_size,
                    letters,
                    word1,
                    word2,
                    word3
                )
                population.sort(
                    key=lambda ind: fitness(ind, word1, word2, word3)
                )
                best_fitness = float('inf')
                stagnation_counter = 0
                reset_counter = 0

            reset_counter += 1

        next_generation = population[:20]  # Elitism: carry over the top 20

        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(population[:50], 2)
            child = crossover(parent1, parent2, word1, word2, word3)
            rand = random.random()

            if rand < 0.2:  # 20% mutation rate
                child = mutate(child, letters, word1, word2, word3)
            if (fitness(child, word1, word2, word3) != float('inf')):
                next_generation.append(child)

        population = next_generation
        # print(len(population))

    print(f"\n\nNo solution found, best fitness:{best_fitness}", end=' ')
    print(f'in generation {generation}')
    return population[0]


if __name__ == "__main__":
    # Example input
    os.system('cls')
    word1 = input("Enter the first word: ").upper()
    word2 = input("Enter the second word: ").upper()
    word3 = input("Enter the result word: ").upper()

    solution = genetic_algorithm(word1, word2, word3)
    val1 = decode(solution, word1)
    val2 = decode(solution, word2)
    val3 = decode(solution, word3)
    if solution:
        print(solution)
        print(f"{word1} + {word2} = {word3}")
        print(f"{val1} + ", end=' ')
        print(f'{val2} = ', end=' ')
        print(f'{val3}, err: {val1 + val2 - val3}')
