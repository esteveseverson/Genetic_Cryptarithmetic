# high fit, better population but slower population gen

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

        if len(set(individual.values())) == len(individual.values()):  # Ensure all values are unique
            # Valida os carry-overs de 10% da população
            if len(population) < int(size * 0.5):
                if fitness(individual, word1, word2, word3) < int(size * 25):
                    # print('bom individuo', individual)
                    population.append(individual)
            else:
                if fitness(individual, word1, word2, word3) < int(size * 60):
                     # print('placebo', individual)
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

    len1, len2 = len(reversed1), len(reversed2)
    carry_over = False
    ok = False
    # Usando o menor comprimento entre as 2 palavras
    shortest_word = min(len1, len2)
    iterator = shortest_word // 2
    for i in range(iterator):
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

def ciclic_crossover(parent1: dict, parent2: dict) -> dict:
    """
    Realiza o crossover cíclico entre dois pais.
    """
    keys = list(parent1.keys())  # Chaves (letras)
    child = {key: None for key in keys}  # Inicializa o filho com valores nulos

    # Inicia ciclo a partir do primeiro índice disponível
    start_index = 0
    while None in child.values():
        current_index = start_index
        visited_keys = set()  # Para rastrear as chaves já visitadas no ciclo

        while True:
            key = keys[current_index]
            if key in visited_keys:
                break
            visited_keys.add(key)
            # Copia o valor do ciclo do pai1
            child[key] = parent1[key]
            # Localiza o próximo índice no ciclo baseado no valor em parent2
            next_value = parent2[key]

            # Verifica se o valor existe no parent1
            matching_key = next(
                (k for k, v in parent1.items() if v == next_value), None
            )
            if matching_key is None:
                break  # Sai do ciclo se não encontrar correspondência

            current_index = keys.index(matching_key)
            if current_index == start_index:
                break

        # Define o próximo índice de início para valores ainda não preenchidos
        for i in range(len(keys)):
            if child[keys[i]] is None:
                start_index = i
                break

    # Preenche os valores restantes do pai2
    for key in keys:
        if child[key] is None:
            child[key] = parent2[key]

    return child


def pmx_crossover(parent1: dict, parent2: dict) -> dict:
    """
    Realiza o crossover PMX entre dois pais.
    """
    keys = list(parent1.keys())
    size = len(keys)
    child = parent1.copy()  # Copia do pai1 para iniciar o filho

    # Seleciona dois pontos de corte
    point1, point2 = sorted(random.sample(range(size), 2))

    # Troca os valores no segmento entre os pontos de corte
    mapping = {}
    for i in range(point1, point2 + 1):
        key = keys[i]
        child[key] = parent2[key]
        mapping[parent2[key]] = parent1[key]

    # Corrige valores duplicados fora do segmento
    for i in range(size):
        if i < point1 or i > point2:
            key = keys[i]
            value = child[key]
            while value in mapping:
                value = mapping[value]
            child[key] = value

    return child

def crossover(parent1: dict, parent2: dict, use_pmx: bool = True) -> dict:
    """
    Seleciona o tipo de crossover entre Cíclico e PMX.
    """
    if use_pmx:
        return pmx_crossover(parent1, parent2)
    else:
        return ciclic_crossover(parent1, parent2)
    

# def crossover(parent1: dict, parent2: dict, word1, word2, word3) -> dict:
#     child = {}
#     for key in parent1.keys():
#         child[key] = parent1[key] if random.random() > 0.5 else parent2[key]

#     if len(set(child.values())) != len(child.values()):
#         return mutate(child, list(child.keys()), word1, word2, word3)  # Mutate if duplicate values are introduced
#     return child


def genetic_algorithm(
    word1: str,
    word2: str,
    word3: str,
    population_size: int = 50,
    generations: int = 100,
    use_tournament: bool = True
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
            if reset_counter >= 3:
                print(f"Population stagnated with {best_fitness} in the {generation} generation. Regenerating new individuals.")
                keep_size = population_size * 0.1
                new_individuals = generate_population(keep_size, letters, word1, word2, word3)
                population = population[:int(keep_size)] + new_individuals
                stagnation_counter = 0
            else:
                print('-' * 20)
                print(f"Population stagnated several times, kill generation {generation}. Start population from begin\n")
                best_from_old_population = population[0]
                population = generate_population(population_size, letters, word1, word2, word3)
                population.append(best_from_old_population)
                stagnation_counter = 0
                reset_counter = 0

            reset_counter += 1

        population.sort(key=lambda ind: fitness(ind, word1, word2, word3))
        next_generation = population[:(int(len(population) * 0.1))]  # Elitism: carry over the top 10%

        while len(next_generation) < population_size:
            # parent1, parent2 = random.sample(population[:15], 2)
            if use_tournament:
                parent1, parent2 = tournament(population, word1, word2, word3)
            else:
                parent1, parent2 = roulette(population, word1, word2, word3)
                
            # child = crossover(parent1, parent2, word1, word2, word3)
            child = crossover(parent1, parent2)
            rand = random.random()

            best_parent_fitness = fitness(parent1, word1, word2, word3) if fitness(parent1, word1, word2, word3) < fitness(parent2, word1, word2, word3) else fitness(parent2, word1, word2, word3)
            # print(best_parent_fitness)
            if rand < 0.2:  # 20% mutation rate
                child = mutate(child, letters, word1, word2, word3)
            if fitness(child, word1, word2, word3) < best_parent_fitness * 5:
                next_generation.append(child)

        population = next_generation

    population.sort(key=lambda ind: fitness(ind, word1, word2, word3))
    print(f"\n\nNo solution found, best fitness:{fitness(population[0], word1, word2, word3)}, in generation {generation}")
    return population[0]

def roulette(population: List[dict], word1: str, word2: str, word3: str) -> List[dict]:
    """
    Seleciona dois indivíduos da população usando o método de roleta.
    """
    # Calcular fitness de todos os indivíduos
    fitness_values = [1 / (1 + fitness(ind, word1, word2, word3)) for ind in population]
    total_fitness = sum(fitness_values)

    # Gerar probabilidades cumulativas
    probabilities = [sum(fitness_values[:i+1]) / total_fitness for i in range(len(fitness_values))]

    def select_one():
        rand = random.random()
        for i, prob in enumerate(probabilities):
            if rand <= prob:
                return population[i]

    # Selecionar dois indivíduos
    parent1 = select_one()
    parent2 = select_one()

    return parent1, parent2


def tournament(population: List[dict], word1: str, word2: str, word3: str, size: int = 3) -> List[dict]:
    """
    Seleciona dois indivíduos da população usando o método de torneio de tamanho 3.
    """
    def select_one():
        # Selecionar aleatoriamente `size` indivíduos
        competitors = random.sample(population, size)
        # Escolher o melhor (menor fitness)
        competitors.sort(key=lambda ind: fitness(ind, word1, word2, word3))
        return competitors[0]

    # Selecionar dois indivíduos
    parent1 = select_one()
    parent2 = select_one()

    return parent1, parent2



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
