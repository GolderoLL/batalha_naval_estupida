from Player_mod import Player
from IA_mod import IAFacil, IAMedio, IADificil
from Tabuleiro_mod import Tabuleiro
from UI_mod import exibir_mensagem_inicio, exibir_mensagem_vitoria, exibir_mensagem_derrota, exibir_mensagem_tiro, exibir_tabuleiros

class Jogo:
    def __init__(self, nome, dificuldade):
        self.player = Player(nome, humano=True)
        self.ia = self.criar_ia_por_dificuldade(dificuldade)

    def preparar_navios(self):
        exibir_mensagem_inicio(self.player.nome)
        self.player.tabuleiro = Tabuleiro()
        self.player.tabuleiro.posicionar_navios_manual()
        self.ia.tabuleiro = Tabuleiro()
        self.ia.tabuleiro.colocar_navios()

    def jogar(self):
        while True:
            exibir_tabuleiros(self.ia.tabuleiro, self.player.tabuleiro, self.player.nome)

            resultado = self.player.movimento(self.ia.tabuleiro)
            exibir_mensagem_tiro(resultado, self.player.nome)
            if self.ia.tabuleiro.navios_afundados():
                exibir_mensagem_vitoria(self.player.nome)
                break

            resultado = self.ia.movimento(self.player.tabuleiro)
            exibir_mensagem_tiro(resultado, self.ia.nome)
            if self.player.tabuleiro.navios_afundados():
                exibir_mensagem_derrota(self.player.nome)
                break
    
    def jogo_acabou(self):
        if not self.player.tabuleiro or not self.ia.tabuleiro:
            return False  # Ainda não iniciou completamente
        return self.player.tabuleiro.navios_afundados() or self.ia.tabuleiro.navios_afundados()

    def criar_ia_por_dificuldade(self, dificuldade):
        if dificuldade == 1:
            return IAFacil("IA Fácil")
        elif dificuldade == 2:
            return IAMedio("IA Média")
        elif dificuldade == 3:
            return IADificil("IA Difícil")

