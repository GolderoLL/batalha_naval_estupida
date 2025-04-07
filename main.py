from Jogo_mod import Jogo
import time
from UI_mod import (
    exibir_titulo,
    barra_de_carregamento,
    solicitar_nome,
    exibir_mensagem_inicio,
    exibir_mensagem_vitoria,
    exibir_mensagem_derrota,
    exibir_tabuleiros,
    exibir_menu,
    exibir_creditos,
    animar_texto,
    escolher_dificuldade,
    tocar_som,
    alternar_som,
)

def main():
    while True:
        exibir_titulo()
        tocar_som("som_intro.mp3")
        opcao = exibir_menu()

        if opcao == "1":
            barra_de_carregamento()
            nome = solicitar_nome()
            exibir_mensagem_inicio(nome)

            dificuldade = escolher_dificuldade()
            jogo = Jogo(nome, dificuldade)
            
            jogo.preparar_navios()

            while not jogo.jogo_acabou():
                exibir_tabuleiros(jogo.ia.tabuleiro, jogo.player.tabuleiro, nome)
                jogo.jogar()

            if jogo.ia.tabuleiro.navios_afundados():
                exibir_mensagem_vitoria(nome)
            else:
                exibir_mensagem_derrota(nome)

        elif opcao == "2":
            exibir_creditos()
        elif opcao == "3":
            alternar_som()
        elif opcao == "4":
            animar_texto("Saindo do jogo. Até logo, comandante!\n")
            break
        else:
            animar_texto("Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    main()