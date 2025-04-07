import numpy as np # type: ignore
import random
from colorama import Fore # type: ignore

class Tabuleiro:
    def __init__(self, tamanho=10):
        self.tamanho = tamanho
        self.tabuleiro = np.zeros((tamanho, tamanho), dtype=int)
        self.navios = [] 


    def posicionar_navio(self, tamanho, linha_inicial, coluna_inicial, orientacao):
            """Posiciona um navio no tabuleiro se possível e registra suas posições."""
            posicoes = []

            for i in range(tamanho):
                if orientacao == 'H':
                    linha = linha_inicial
                    coluna = coluna_inicial + i
                else:
                    linha = linha_inicial + i
                    coluna = coluna_inicial

                if not (0 <= linha < self.tamanho and 0 <= coluna < self.tamanho):
                    return False
                if self.tabuleiro[linha, coluna] != 0:
                    return False

                posicoes.append((linha, coluna))

            for linha, coluna in posicoes:
                self.tabuleiro[linha, coluna] = 1

            self.navios.append(posicoes)
            return True

    def colocar_navios(self):
        tamanhos_navios = [5, 4, 3, 3, 2]  
        for tamanho_navio in tamanhos_navios:
            colocado = False
            while not colocado:
                orientacao = random.choice(['H', 'V'])
                linha = random.randint(0, self.tamanho - 1)
                coluna = random.randint(0, self.tamanho - 1)
                colocado = self.posicionar_navio(tamanho_navio, linha, coluna, orientacao)

    def posicionar_navios_manual(self):
        print("Hora de posicionar seus navios!")
        tamanhos_navios = [5, 4, 3, 3, 2]  
        for tamanho_navio in tamanhos_navios:
            colocado = False
            while not colocado:
                print(f"\nNavio de tamanho {tamanho_navio}")
                linha = self.receber_input_valido(0, self.tamanho - 1, "Linha inicial: ")
                coluna = self.receber_input_valido(0, self.tamanho - 1, "Coluna inicial: ")
                orientacao = input("Orientação (H para horizontal, V para vertical): ").upper()

                if orientacao not in ['H', 'V']:
                    print("Orientação inválida. Use H ou V.")
                    continue

                if self.posicionar_navio(tamanho_navio, linha, coluna, orientacao):
                    colocado = True
                    print("Navio colocado:")
                    print(self.exibir_completo())
                else:
                    print("Não foi possível posicionar o navio. Tente novamente.")

    def receber_input_valido(self, minimo, maximo, mensagem):
        while True:
            try:
                valor = int(input(mensagem))
                if minimo <= valor <= maximo:
                    return valor
                else:
                    print(f"Digite um valor entre {minimo} e {maximo}.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")
    
    def receber_tiro(self, linha, coluna):
        if self.tabuleiro[linha, coluna] == 1:
            self.tabuleiro[linha, coluna] = -1  # Acertou
            return 1
        elif self.tabuleiro[linha, coluna] == 0:
            self.tabuleiro[linha, coluna] = -2  # Erro
            return 2
        else:
            return 3  # Já atirou aqui
    
    def exibir_oculto(self):
        visao = np.full((self.tamanho, self.tamanho), '*', dtype=str)
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.tabuleiro[i, j] == -1:
                 visao[i, j] = '!'  # Acerto
                elif self.tabuleiro[i, j] == -2:
                 visao[i, j] = 'X'  # Erro
        return self.formatar_tabuleiro(visao)

    def exibir_completo(self):
        visao = np.full((self.tamanho, self.tamanho), '*', dtype=str)
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.tabuleiro[i, j] == 1:
                    visao[i, j] = '■'  # Navio
                elif self.tabuleiro[i, j] == -1:
                    visao[i, j] = '!'
                elif self.tabuleiro[i, j] == -2:
                    visao[i, j] = 'X'
        return self.formatar_tabuleiro(visao)

    def formatar_tabuleiro(self, matriz_visao):
        resultado = "   " + " ".join(str(i) for i in range(self.tamanho)) + "\n"
        for i in range(self.tamanho):
            linha = f"{i}  "
            for j in range(self.tamanho):
                simbolo = matriz_visao[i][j]
                if simbolo == '■':
                    cor = Fore.CYAN
                elif simbolo == '!':
                    cor = Fore.RED
                elif simbolo == 'X':
                    cor = Fore.YELLOW
                else:
                    cor = Fore.WHITE
                linha += cor + simbolo + " "
            resultado += linha + "\n"
        return resultado

    def navios_afundados(self):
            return not np.any(self.tabuleiro == 1)
    
    def get_navio_em(self, posicao):
        """Retorna o navio (lista de posições) ao qual a posição pertence, se existir."""
        for navio in self.navios:
            if posicao in navio:
                return navio
        return []