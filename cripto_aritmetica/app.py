import random
import itertools

# Função de fitness: calcula o erro absoluto da equação
# |(SEND + MORE) - MONEY|
def calcular_fitness(individuo, letras, palavras):
    letter_to_digit = dict(zip(letras, individuo))

    def palavra_para_numero(palavra):
        # Converter palavra em número, verificando se não há zeros à esquerda
        numero = ''.join(str(letter_to_digit[letra]) for letra in palavra)
        if numero[0] == '0':
            return None
        return int(numero)

    valores_palavras = [palavra_para_numero(palavra) for palavra in palavras]

    # Verificar se algum número é inválido (zeros à esquerda)
    if None in valores_palavras:
        return float('inf')

    soma = sum(valores_palavras[:-1])
    resultado = valores_palavras[-1]
    return abs(soma - resultado)

# Gerar população inicial (aleatória, sem repetições)
def gerar_populacao_inicial(tamanho, letras):
    populacao = []
    while len(populacao) < tamanho:
        individuo = random.sample(range(10), len(letras))
        if individuo not in populacao:
            populacao.append(individuo)
    return populacao

# Seleção por torneio (tamanho = 3)
def selecao_torneio(populacao, fitness, k=3):
    torneio = random.sample(list(zip(populacao, fitness)), k)
    return min(torneio, key=lambda x: x[1])[0]

# Seleção por roleta
def selecao_roleta(populacao, fitness):
    fitness_normalizado = [1 / (f + 1e-6) for f in fitness]
    total_fitness = sum(fitness_normalizado)
    probabilidades = [f / total_fitness for f in fitness_normalizado]
    acumulada = list(itertools.accumulate(probabilidades))
    r = random.uniform(0, 1)
    for i, valor in enumerate(acumulada):
        if r <= valor:
            return populacao[i]

# Mutação: troca de duas posições no vetor
def mutacao(individuo, taxa):
    if random.random() < taxa:
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

# Crossover PMX
def crossover_pmx(pai1, pai2):
    size = len(pai1)
    filho = [-1] * size

    # Escolher dois pontos de crossover
    p1, p2 = sorted(random.sample(range(size), 2))

    # Copiar segmento do pai1 para o filho
    filho[p1:p2 + 1] = pai1[p1:p2 + 1]

    # Resolver conflitos e preencher os valores restantes
    for i in range(p1, p2 + 1):
        if pai2[i] not in filho:
            val = pai2[i]
            pos = i
            while True:
                if pai1[pos] in pai2:
                    pos = pai2.index(pai1[pos])
                    if filho[pos] == -1:
                        filho[pos] = val
                        break
                else:
                    break

    # Preencher os espaços vazios com o restante do pai2
    for i in range(size):
        if filho[i] == -1:
            filho[i] = pai2[i]

    return filho

# Crossover Cíclico (CX)
def crossover_ciclico(pai1, pai2):
    size = len(pai1)
    filho = [-1] * size
    start = 0

    while -1 in filho:
        if filho[start] == -1:
            pos = start
            while True:
                filho[pos] = pai1[pos]
                if pai2[pos] in pai1:
                    pos = pai1.index(pai2[pos])
                    if pos == start:
                        break
                else:
                    break
        start += 1

    for i in range(size):
        if filho[i] == -1:
            filho[i] = pai2[i]

    return filho

# Algoritmo Genético Principal
def algoritmo_genetico(palavras, geracoes=50, tamanho_pop=100, taxa_crossover=0.8, taxa_mutacao=0.1):
    letras = ''.join(set(''.join(palavras)))
    assert len(letras) <= 10, "Mais de 10 letras únicas não suportadas."

    # Gerar população inicial
    populacao = gerar_populacao_inicial(tamanho_pop, letras)

    for geracao in range(geracoes):
        # Avaliar fitness de cada indivíduo
        fitness = [calcular_fitness(individuo, letras, palavras) for individuo in populacao]

        # Verificar se alguma solução foi encontrada
        if 0 in fitness:
            melhor_individuo = populacao[fitness.index(0)]
            return dict(zip(letras, melhor_individuo))

        # Nova população com elitismo
        nova_populacao = []
        elitismo = sorted(zip(populacao, fitness), key=lambda x: x[1])[:2]
        nova_populacao.extend([ind[0] for ind in elitismo])

        # Seleção, crossover e mutação
        while len(nova_populacao) < tamanho_pop:
            pai1 = selecao_roleta(populacao, fitness)
            pai2 = selecao_roleta(populacao, fitness)

            if random.random() < taxa_crossover:
                filho = crossover_pmx(pai1, pai2)
            else:
                filho = crossover_ciclico(pai1, pai2)

            filho = mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)

        populacao = nova_populacao

    # Retornar melhor solução encontrada ao final das gerações
    fitness = [calcular_fitness(individuo, letras, palavras) for individuo in populacao]
    melhor_individuo = populacao[fitness.index(min(fitness))]
    return dict(zip(letras, melhor_individuo))

# Testar o algoritmo com o problema SEND + MORE = MONEY
if __name__ == "__main__":
    palavras = ["SEND", "MORE", "MONEY"]
    solucao = algoritmo_genetico(palavras)

    if solucao:
        print("Solução encontrada:")
        for letra, valor in solucao.items():
            print(f"{letra}: {valor}")

        send = int(''.join(str(solucao[letra]) for letra in "SEND"))
        more = int(''.join(str(solucao[letra]) for letra in "MORE"))
        money = int(''.join(str(solucao[letra]) for letra in "MONEY"))

        print(f"\nSEND: {send}\nMORE: {more}\nMONEY: {money}")
        print(f"\nVerificação: {send} + {more} = {money}")
    else:
        print("Nenhuma solução encontrada.")
