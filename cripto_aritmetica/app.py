# execute whole options

import time
from openpyxl import Workbook
from cripto_aritmetica.ciclic_crossover import decode, genetic_algorithm


def run_experiment():
    word1 = "SEND"
    word2 = "MORE"
    word3 = "MONEY"

    population_size = 100
    generations = 1000

    crossover_rates = [0.6, 0.8]
    mutation_rates = [0.05, 0.1]
    selection_methods = ["Roulette", "Tournament"]
    crossover_types = ["Cyclic", "PMX"]
    reinsertion_methods = ["Ordered", "Elitism"]

    results = []
    wb = Workbook()
    ws = wb.active
    ws.append(["TAXA CROSSOVER", "TAXA MUTAÇÃO", "SELEÇÃO", "CROSSOVER", "REINSERÇÃO", "RESULTADO"])

    for crossover_rate in crossover_rates:
        for mutation_rate in mutation_rates:
            for selection_method in selection_methods:
                for crossover_type in crossover_types:
                    for reinsertion_method in reinsertion_methods:

                        # Configurações
                        use_tournament = selection_method == "Tournament"
                        use_pmx = crossover_type == "PMX"
                        use_elitism = reinsertion_method == "Elitism"

                        start_time = time.time()

                        # Executa o algoritmo genético
                        solution, generation_found = genetic_algorithm(
                            word1,
                            word2,
                            word3,
                            population_size=population_size,
                            generations=generations,
                            use_tournament=use_tournament,
                            use_elitism=use_elitism,
                            use_pmx=use_pmx
                        )

                        end_time = time.time()
                        elapsed_time = end_time - start_time

                        # Decodifica e verifica solução
                        val1 = decode(solution, word1)
                        val2 = decode(solution, word2)
                        val3 = decode(solution, word3)

                        if abs((val1 + val2) - val3) == 0:
                            result = f"Geração encontrada: {generation_found}"
                        else:
                            result = "Não encontrou solução"

                        # Salva resultado
                        results.append([
                            crossover_rate,
                            mutation_rate,
                            selection_method,
                            crossover_type,
                            reinsertion_method,
                            result
                        ])

                        # Adiciona ao Excel
                        ws.append([
                            crossover_rate,
                            mutation_rate,
                            selection_method,
                            crossover_type,
                            reinsertion_method,
                            result
                        ])

    # Salva os resultados no arquivo Excel
    wb.save("resultados_ag.xlsx")


if __name__ == "__main__":
    run_experiment()
