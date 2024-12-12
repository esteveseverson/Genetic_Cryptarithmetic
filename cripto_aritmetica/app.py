import itertools
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


def verificar_equacao(letters, valores, palavras):
    # Mapeando as letras para os valores correspondentes
    letter_to_digit = dict(zip(letters, valores))

    # Função para converter uma palavra de letras para número
    def palavra_para_numero(palavra):
        return int(''.join(str(letter_to_digit[letra]) for letra in palavra))

    # Convertendo as palavras para números
    valores_palavras = [palavra_para_numero(palavra) for palavra in palavras]

    soma = sum(valores_palavras[:-1])
    resultado = valores_palavras[-1]

    return soma, resultado


def criptoaritmetica(palavras):
    # Extraindo as letras únicas das palavras
    letras = ''.join(palavras)
    letras_unicas = set(letras)  # Retira letras repetidas
    assert len(letras_unicas) <= 10, 'Há mais de 10 letras diferentes!'

    # Identificando as letras que estão no início de cada palavra
    letras_iniciais = {palavra[0] for palavra in palavras}

    # Gerando todas as permutações possíveis para as letras
    for perm in itertools.permutations(range(10), len(letras_unicas)):
        # Verificando se as letras iniciais não são 0
        letter_to_digit = dict(zip(letras_unicas, perm))
        if any(letter_to_digit[letra] == 0 for letra in letras_iniciais):
            continue

        # Verificando a equação com essa permutação
        soma, resultado = verificar_equacao(letras_unicas, perm, palavras)

        # Se a equação for válida, imprime o resultado
        if soma == resultado:
            # Exibindo as palavras e os valores das letras
            print('Palavras e Valores:')
            for i, palavra in enumerate(palavras):
                # Imprimindo a palavra seguida pelos valores
                print(f'{" ".join(palavra)}', end='\t\t')
                print(
                    f'{" ".join(str(letter_to_digit[letra]) for letra in palavra)}'
                )

                if i == len(palavras) - 2:
                    print('-' * (len(palavras[-1]) * 7))

            # Exibindo a solução
            return

    print('Nenhuma solução encontrada.')


def menu():
    while True:
        # Exibe o menu
        print("\nMenu:")
        print("1. Inserir palavras e resolver criptaritimética")
        print("2. Sair")

        # Obtém a escolha do usuário
        escolha = prompt("Escolha uma opção: ")

        if escolha == "1":
            # O usuário insere as palavras
            palavras_input = prompt("Digite as palavras separadas por espaço: ")

            # Separa as palavras
            palavras = palavras_input.split()

            # Executa a função de criptoaritmética
            criptoaritmetica(palavras)
        
        elif escolha == "2":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
