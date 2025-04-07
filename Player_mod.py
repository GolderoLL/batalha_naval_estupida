from Tabuleiro_mod import Tabuleiro
import random
from UI_mod import animar_texto, exibir_mensagem_tiro, solicitar_nome

class Player:
    def __init__(self, nome, humano=True):
        self.nome = nome
        self.tabuleiro = Tabuleiro()
        self.humano = humano

    def movimento(self, tabuleiro_inimigo):
        if self.humano:
            while True:
                try:
                    linha = int(input(f'{self.nome}, digite a linha do seu ataque! (0 a {self.tabuleiro.tamanho - 1}): '))
                    coluna = int(input(f'{self.nome}, digite a coluna do seu ataque! (0 a {self.tabuleiro.tamanho - 1}): '))
                    if linha < 0 or linha > 9 or coluna < 0 or coluna > 9:
                        animar_texto("Posição inválida! Tente novamente.", delay=0.02)
                        continue
                    resultado = tabuleiro_inimigo.receber_tiro(linha, coluna)
                    if resultado == 3:
                        animar_texto("Você já atirou aqui! Tente novamente.", delay=0.02)
                        continue
                    return resultado
                except ValueError:
                    animar_texto("Valor inválido! Tente novamente com números inteiros.", delay=0.02)
        else:
            while True:
                i = random.randint(0, 4)
                j = random.randint(0, 4)
                resultado = tabuleiro_inimigo.receber_tiro(i, j)
                if resultado != 3:
                    print(f'{self.nome} atacou ({i}, {j})')
                    return resultado