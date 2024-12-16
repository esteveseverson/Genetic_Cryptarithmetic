# Brute force solver

import itertools
import os

from prompt_toolkit import print_formatted_text as print_text
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style


# Função para limpar a tela
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# Estilo para as entradas
style = Style.from_dict({
    'input': 'fg:cyan bold',
    'output': 'fg:green',
    'menu': 'fg:yellow',
})


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
            print_text(HTML('<bold><green>Palavras e Valores:</green></bold>'))
            for i, palavra in enumerate(palavras):
                # Imprimindo a palavra seguida pelos valores
                print_text(
                    f'{" ".join(palavra)}\t\t{" ".join(
                        str(letter_to_digit[letra]
                        ) for letra in palavra
                        )}'
                )

                if i == len(palavras) - 2:
                    print('-' * (len(palavras[-1]) * 7))

            # Espera o usuário pressionar qualquer tecla para voltar
            prompt("Pressione qualquer tecla para voltar ao menu...")
            return

    # Se não encontrar solução
    print_text(HTML('<bold><red>Nenhuma solução encontrada.</red></bold>'))
    prompt("Pressione qualquer tecla para voltar ao menu...")


def menu():
    while True:
        # Exibe o menu com cores
        limpar_tela()
        print_text(HTML(
            '<bold><yellow>Menu:</yellow></bold>'
        ))
        print_text(HTML(
            '<green>1. Inserir palavras e resolver criptaritimética</green>'
        ))
        print_text(HTML(
            '<green>2. Sair</green>')
        )

        escolha = prompt("Escolha uma opção: ", style=style)

        if escolha == "1":
            limpar_tela()
            palavras = []
            for i in range(3):  # Solicita exatamente 3 palavras
                while True:
                    palavra = prompt(
                        f"Digite a {i + 1}ª palavra: ", style=style
                    )
                    if palavra.isalpha():
                        # Adiciona palavra em maiúsculas
                        palavras.append(palavra.upper())  
                        print_text(
                            HTML(
                                f'<bold>
                                <cyan>
                                Palavra {palavra} adicionada com sucesso!
                                </cyan>
                                </bold>'
                            )
                        )
                        break
                    else:
                        print_text(HTML(
                            '''
                            <bold>
                            <red>
                            Por favor, insira apenas letras na palavra!
                            </red>
                            </bold>
                            '''
                        ))

            limpar_tela()
            print_text(HTML(
                '<bold><yellow>Processando Requisição...</yellow></bold>')
            )
            # Resolve a criptoaritmética com as palavras inseridas
            criptoaritmetica(palavras)  

        elif escolha == "2":
            print_text(HTML('<bold><yellow>Saindo...</yellow></bold>'))
            break

        else:
            limpar_tela()
            print_text(HTML(
                '<bold><red>Opção inválida. Tente novamente.</red></bold>'
            ))


if __name__ == "__main__":
    menu()
