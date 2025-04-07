from Player_mod import Player
import random

class IA(Player):
    def __init__(self, nome="IA"):
        super().__init__(nome, humano=False)    
        self.tentou = set()

    def movimento(self, tabuleiro_inimigo):
        raise NotImplementedError("Subclasse deve implementar este método.")

class IAFacil(IA):
    def movimento(self, tabuleiro_inimigo, nome="IA Fácil"):
        while True:
            linha = random.randint(0, tabuleiro_inimigo.tamanho - 1)
            coluna = random.randint(0, tabuleiro_inimigo.tamanho - 1)
            if (linha, coluna) not in self.tentou:
                self.tentou.add((linha, coluna))
                print(f'{self.nome} (Fácil) atirou em {linha}, {coluna}!')
                return tabuleiro_inimigo.receber_tiro(linha, coluna)

class IAMedio(IA):
    def __init__(self, nome="IA Média"):
        super().__init__(nome)
        self.acertos = []

    def posicoes_adjacentes(self, linha, coluna):
        return [
            (linha - 1, coluna),
            (linha + 1, coluna),
            (linha, coluna - 1),
            (linha, coluna + 1)
        ]

    def movimento(self, tabuleiro_inimigo):
        if self.acertos:
            adjacentes = []
            for l, c in self.acertos:
                adjacentes += self.posicoes_adjacentes(l, c)
            random.shuffle(adjacentes)
            for linha, coluna in adjacentes:
                if 0 <= linha < tabuleiro_inimigo.tamanho and 0 <= coluna < tabuleiro_inimigo.tamanho:
                    if (linha, coluna) not in self.tentou:
                        self.tentou.add((linha, coluna))
                        resultado = tabuleiro_inimigo.receber_tiro(linha, coluna)
                        print(f'{self.nome} (Médio) atirou em {linha}, {coluna}!')
                        if resultado == 1:
                            self.acertos.append((linha, coluna))
                        return resultado
        # Se não acertou antes ou não tem adjacentes válidos, atira aleatoriamente
        while True:
            linha = random.randint(0, tabuleiro_inimigo.tamanho - 1)
            coluna = random.randint(0, tabuleiro_inimigo.tamanho - 1)
            if (linha, coluna) not in self.tentou:
                self.tentou.add((linha, coluna))
                resultado = tabuleiro_inimigo.receber_tiro(linha, coluna)
                print(f'{self.nome} (Médio) atirou em {linha}, {coluna}!')
                if resultado == 1:
                    self.acertos.append((linha, coluna))
                return resultado

class IADificil(IA):
    def __init__(self, nome="IA Difícil"):
        super().__init__(nome)
        self.acertos = []
        self.direcao = None
        self.modo = 'caça'
    
    def posicao_adjacente(self, linha, coluna):
        posicoes = []
        if linha > 0:
            posicoes.append((linha - 1, coluna))
        if linha < self.tabuleiro.tamanho - 1:
            posicoes.append((linha + 1, coluna))
        if coluna > 0:
            posicoes.append((linha, coluna - 1))
        if coluna < self.tabuleiro.tamanho - 1:
            posicoes.append((linha, coluna + 1))
        return posicoes
    
    def pegar_direcoes_posicionais(self):
        if len(self.acertos) < 2:
            return []
        
        (linha1, coluna1), (linha2, coluna2) = self.acertos[0], self.acertos[1]
        if linha1 == linha2:
            self.direcao = 'horizontal'
        elif coluna1 == coluna2:
            self.direcao = 'vertical'
        else:
            return []
        
        tentar = []
        self.acertos.sort()
        if self.direcao == 'horizontal':
            linhas = self.acertos[0][0]
            colunas = [col for _, col in self.acertos]
            if min(colunas) > 0:
                tentar.append((linhas, min(colunas) - 1))
            if max(colunas) < self.tabuleiro.tamanho - 1:
                tentar.append((linhas, max(colunas) + 1))
        else:
            colunas = self.acertos[0][1]
            linhas = [lin for _, lin in self.acertos]
            if min(linhas) > 0:
                tentar.append((min(linhas) - 1, colunas))
            if max(linhas) < self.tabuleiro.tamanho - 1:
                tentar.append((min(linhas) + 1, colunas))
        return tentar
    
    def posicoes_xadrez(self):
        for linhas in range(self.tabuleiro.tamanho):
            for colunas in range(self.tabuleiro.tamanho):
                if (linhas + colunas) % 2 == 0:
                    yield (linhas, colunas)
    
    def movimento(self, tabuleiro_inimigo):
        if self.modo == 'alvo' and self.acertos:
            posicoes = self.pegar_direcoes_posicionais() or sum([self.posicao_adjacente(linhas, colunas) for linhas, colunas in self.acertos], [])
            random.shuffle(posicoes)
            for linhas, colunas in posicoes:
                if (linhas, colunas) not in self.tentou:
                    self.tentou.add((linhas, colunas))
                    resultado = tabuleiro_inimigo.receber_tiro(linhas, colunas)
                    print(f'{self.nome} atirou em {linhas}, {colunas}!')
                    if resultado == 1:
                       self.acertos.append((linhas, colunas))
                    elif resultado == 2:
                        pass
                    if not tabuleiro_inimigo.navios_afundados():
                        return resultado
                    if resultado == 1:
                        return resultado
                    break
                else:
                    self.acertos.clear()
                    self.direcao = None
                    self.modo = 'caça'
        if self.modo == 'caça' or not self.acertos:
            for linhas, colunas in self.posicoes_xadrez():
                if (linhas, colunas) not in self.tentou:
                    self.tentou.add((linhas, colunas))
                    resultado = tabuleiro_inimigo.receber_tiro(linhas, colunas)
                    print(f'{self.nome} atirou em {linhas}, {colunas}!')
                    if resultado == 1:
                        self.acertos = [(linhas, colunas)]
                        self.modo = 'alvo'
                    return resultado