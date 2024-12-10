import itertools

def verificar_equacao(letters, valores, palavras):
    # Mapeando as letras para os valores correspondentes
    letter_to_digit = dict(zip(letters, valores))
    
    # Função para converter uma palavra de letras para número
    def palavra_para_numero(palavra):
        return int(''.join(str(letter_to_digit[letra]) for letra in palavra))
    
    # Convertendo as palavras para números
    valores_palavras = [palavra_para_numero(palavra) for palavra in palavras]
    
    # Retornando a soma de todos os números (exceto o último, que é o resultado)
    return sum(valores_palavras[:-1]), valores_palavras[-1]

def criptoaritmetica(palavras):
    # Extraindo as letras únicas das palavras
    letras = ''.join(palavras)
    letras_unicas = set(letras)  # Retira letras repetidas
    assert len(letras_unicas) <= 10, "Há mais de 10 letras diferentes!"
    
    # Identificando as letras que estão no início de cada palavra
    letras_iniciais = {palavra[0] for palavra in palavras}

    # Gerando todas as permutações possíveis para as letras
    for perm in itertools.permutations(range(10), len(letras_unicas)):
        # Verificando se as letras iniciais não são 0
        letter_to_digit = dict(zip(letras_unicas, perm))
        if any(letter_to_digit[letra] == 0 for letra in letras_iniciais):
            continue  # Se alguma das letras iniciais for 0, pula essa permutação
        
        # Verificando a equação com essa permutação
        soma, resultado = verificar_equacao(letras_unicas, perm, palavras)
        
        # Calculando o erro
        erro = abs(resultado - soma)
        
        # Se a equação for válida, imprime o resultado
        if soma == resultado:
            # Exibindo as palavras e os valores das letras
            print("Palavras:")
            for palavra in palavras:
                print(palavra)
            print()

            print("Valores:")
            for palavra in palavras:
                print(' '.join(str(letter_to_digit[letra]) for letra in palavra))
            print("-" * 15)

            print("Resultado:")
            print(' '.join(str(letter_to_digit[letra]) for letra in palavras[-1]))
            print()

            return
    
    print("Nenhuma solução encontrada.")

# Rodando a função com as palavras do exemplo SEND + MORE = MONEY
palavras = ["PARA", "AMAPA", "GOIAS"]
criptoaritmetica(palavras)
