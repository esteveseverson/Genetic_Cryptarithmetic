# high fight, better population but slower population gen

import os
import random
from typing import List, Tuple, Dict

def generate_population(
    size: int, 
    letters: List[str], 
    word1: str, 
    word2: str, 
    word3: str,
) -> List[dict] :
    population = []

    while len(population) < size:
        individual = {}
        values = random.sample(range(10), len(letters))
        for letter, value in zip(letters, values):
            individual[letter] = value

        if len(set(individual.values())) == len(individual.values()):  # Ensure all values are unique
            # Valida os carry-overs de 20% da população
            if len(population) < int(size * 0.2):
                if validate_carry_overs(individual, word1, word2, word3) == float('inf'):
                    # print('carry over problem')
                    continue
            
            if fitness(individual, word1, word2, word3) != float('inf'):
                # ('gerou uma população')
                population.append(individual)
                
        # print(len(population))
    return population

def decode(individual: dict, word: str) -> int:
    return int(''.join(str(individual[letter]) for letter in word))

def fitness(individual: dict, word1: str, word2: str, word3: str) -> float:

    # Garante que todas as letras tenham valores únicos
    if len(set(individual.values())) != len(individual.values()):
        # print('not unique values')
        return float('inf')
    
    # Garante que as primeiras letras não sejam zero
    if individual[word1[0]] == 0 or individual[word2[0]] == 0 or individual[word3[0]] == 0:
        # print('stars with 0')
        return float('inf')

    # sums of the last values 1 and 2 has to be de 3
    if individual[word1[-1]] + individual[word2[-1]] >= 10:
        if ((individual[word1[-1]] + individual[word2[-1]]) - 10) != individual[word3[-1]]:
            return float('inf')
    else:
        if individual[word1[-1]] + individual[word2[-1]] != individual[word3[-1]]:
            return float('inf')

    # print('all validations check')
    # Decodifica palavras em valores numéricos
    val1 = decode(individual, word1)
    val2 = decode(individual, word2)
    val3 = decode(individual, word3)

    # Retorna a pontuação de fitness como a diferença absoluta
    # print('retornou valor')
    return abs((val1 + val2) - val3)

def validate_carry_overs(individual: dict, word1: str, word2: str, word3: str) -> bool:

    def carry_over_check(carry_over: bool, id_sum: int, target: int):
        
        if carry_over:
            id_sum += 1
            if id_sum >= 10:
                carry_over_return = True
                if id_sum != target:
                    return carry_over_return, float('inf')
                
            if id_sum < 10:
                carry_over_return = False
                if id_sum != target:
                    return carry_over_return, float('inf')

            
        if not carry_over:
            if id_sum >= 10:
                carry_over_return = True
                if id_sum != target:
                    return carry_over_return, float('inf')
                
            if id_sum < 10:
                carry_over_return = False
                if id_sum != target:
                    return carry_over_return, float('inf')
                
        return carry_over_return, 0
    
    reversed1 = word1[::-1]
    reversed2 = word2[::-1]
    reversed3 = word3[::-1]

    len1, len2, len3 = len(reversed1), len(reversed2), len(reversed3)
    carry_over = False
    ok = False
    # Usando o menor comprimento entre as 2 palavras
    for i in range((min(len1, len2) // 2) + 1):
        id_sum = individual[reversed1[i]] + individual[reversed2[i]]
        target = individual[reversed3[i]]
        
        carry_over, value = carry_over_check(carry_over, id_sum, target)
        if value == float('inf'):
            # print('quebrou o carry over')
            return value
        
    ok = True
    # print('carry over check')
    return ok


def mutate(individual: dict, letters: List[str], word1: str, word2: str, word3: str) -> dict:
    mutated = individual.copy()
    letter = random.choice(letters)
    new_value = random.choice([i for i in range(10) if i not in individual.values()])
    while mutated == individual:
        mutated[letter] = new_value
        if fitness(mutated, word1, word2, word3) == float('inf'):
            mutated == individual
    return mutated


def crossover(parent1: dict, parent2: dict, word1, word2, word3) -> dict:
    child = {}
    for key in parent1.keys():
        child[key] = parent1[key] if random.random() > 0.5 else parent2[key]

    if len(set(child.values())) != len(child.values()):
        return mutate(child, list(child.keys()), word1, word2, word3)  # Mutate if duplicate values are introduced
    return child

def genetic_algorithm(
    word1: str, 
    word2: str, 
    word3: str, 
    population_size: int = 50, 
    generations: int = 100,
):
    letters = list(set(word1 + word2 + word3))
    if len(letters) > 10:
        raise ValueError("Maximum of 10 unique letters allowed.")

    population = generate_population(population_size, letters, word1, word2, word3)
    stagnation_counter = 0
    reset_counter = 0
    best_fitness = float('inf')
    last_best_fitness = float('inf')

    for generation in range(generations):
        population.sort(key=lambda ind: fitness(ind, word1, word2, word3))
        best_fitness = fitness(population[0], word1, word2, word3)
        
        if best_fitness == 0:
            print(f"\n\nSolution found with {best_fitness} fitness, in generation {generation}")
            return population[0]

        # Check for stagnation
        if best_fitness == last_best_fitness:
            stagnation_counter += 1
        else:
            stagnation_counter = 0
            last_best_fitness = best_fitness

        if stagnation_counter >= int(generations * 0.07):
            if reset_counter >= int(generations * 0.4):
                print(f"Population stagnated with {best_fitness} in the {generation} generation. Regenerating new individuals.")
                keep_size = population_size * 0.1
                new_individuals = generate_population(keep_size, letters, word1, word2, word3)
                population = population[:int(keep_size)] + new_individuals
                population.sort(key=lambda ind: fitness(ind, word1, word2, word3))
                stagnation_counter = 0
            else:
                print('-' * 20)
                print(f"Population stagnated several times, kill generation {generation}. Start population from begin\n")
                best_from_old_population = population[0]
                population = generate_population(population_size - 1, letters, word1, word2, word3)
                population.append(best_from_old_population)
                population.sort(key=lambda ind: fitness(ind, word1, word2, word3))
                best_fitness = float('inf')
                stagnation_counter = 0
                reset_counter = 0
                
            reset_counter += 1

        next_generation = population[:(int(len(population) * 0.1))]  # Elitism: carry over the top 10%

        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(population[:15], 2)
            child = crossover(parent1, parent2, word1, word2, word3)
            rand = random.random()
            
            if rand < 0.2:  # 20% mutation rate
                child = mutate(child, letters, word1, word2, word3)
            if (fitness(child, word1, word2, word3) != float('inf')):
                next_generation.append(child)

        population = next_generation
        # print(len(population))

    print(f"\n\nNo solution found, best fitness:{best_fitness}, in generation {generation}")
    return population[0]

if __name__ == "__main__":
    # Example input
    os.system('cls')
    word1 = input("Enter the first word: ").upper()
    word2 = input("Enter the second word: ").upper()
    word3 = input("Enter the result word: ").upper()

    solution = genetic_algorithm(word1, word2, word3)
    if solution:
        print("Solution:", solution)
        print(f"{word1} + {word2} = {word3}")
        print(f"{decode(solution, word1)} + {decode(solution, word2)} = {decode(solution, word3)}")
