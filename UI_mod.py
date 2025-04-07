import time
import sys
import os
try:
    from playsound import playsound # type: ignore
except ImportError:
    playsound = None  # Evita erro caso playsound não esteja instalado

som_ativado = True

from colorama import init, Fore, Style # type: ignore
init(autoreset=True)

def animar_texto(texto, delay=0.03, cor=Fore.WHITE):
    for caractere in texto:
        sys.stdout.write(cor + caractere)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def barra_de_carregamento(segundos=3):
    print(Fore.CYAN + "Preparando a Batalha Naval:")
    for i in range(0, 21):
        bar = '#' * i + '-' * (20 - i)
        sys.stdout.write(Fore.GREEN + f"\r[{bar}] {i * 5}%")
        sys.stdout.flush()
        time.sleep(segundos / 20)
    print("\n")


def tocar_som(nome_arquivo):
    global som_ativado
    if not som_ativado:
        return
    caminho_arquivo = os.path.join(os.path.dirname(__file__), nome_arquivo)
    if not os.path.exists(caminho_arquivo):
        print(Fore.YELLOW + f"[AVISO] Arquivo de som não encontrado: {caminho_arquivo}")
        return
    try:
        playsound(caminho_arquivo)
    except Exception as e:
        print(Fore.YELLOW + f"[AVISO] Não foi possível tocar o som: {e}")

def alternar_som():
    global som_ativado
    som_ativado = not som_ativado
    estado = "ativado" if som_ativado else "desativado"
    animar_texto(f"Som {estado} com sucesso!", cor=Fore.YELLOW)
    time.sleep(1.5)

def exibir_titulo():
    print(Fore.MAGENTA + """
 ,---.     .--.  _______  .--.  ,-.    .-. .-.  .--.    .-. .-.  .--..-.   .-..--.  ,-.     
 | .-\.   / /\ \|__   __|/ /\ \ | |    | | | | / /\ \   |  \| | / /\ \\ \ / // /\ \ | |     
 | |-' \ / /__\ \ )| |  / /__\ \| |    | `-' |/ /__\ \  |   | |/ /__\ \\ V // /__\ \| |     
 | |--. \|  __  |(_) |  |  __  || |    | .-. ||  __  |  | |\  ||  __  | ) / |  __  || |     
 | |`-' /| |  |)|  | |  | |  |)|| `--. | | |)|| |  |)|  | | |)|| |  |)|(_)  | |  |)|| `--.  
 /( `--' |_|  (_)  `-'  |_|  (_)|( __.'/(  (_)|_|  (_)  /(  (_)|_|  (_)     |_|  (_)|( __.' 
(__)                            (_)   (__)             (__)                         (_)         
""")

def exibir_mensagem_inicio(nome):
    animar_texto(f"Prepare seus navios, Almirante {nome}!\n", delay=0.04, cor=Fore.CYAN)

def exibir_mensagem_vitoria(nome):
    animar_texto(f"Parabéns, Almirante {nome}, você venceu!\n", delay=0.04, cor=Fore.GREEN)
    tocar_som("som_vitoria.mp3")

def exibir_mensagem_derrota(nome):
    animar_texto(f"Game Over, Almirante {nome}, você perdeu...\n", delay=0.04, cor=Fore.RED)
    tocar_som("som_derrota.mp3")

def exibir_mensagem_tiro(resultado, atacante):
    if resultado == 1:
        tocar_som("som_acerto.mp3")
        animar_texto(f"{atacante}: BOOM! Alvo atingido!\n", cor=Fore.GREEN)
    elif resultado == 2:
        tocar_som("som_erro.mp3")
        animar_texto(f"{atacante}: Splash... Água.\n", cor=Fore.BLUE)
    elif resultado == 3:
        animar_texto(f"{atacante}: Tiro repetido. Escolha outro alvo.\n", cor=Fore.YELLOW)

def exibir_tabuleiros(tabuleiro_ia, tabuleiro_player, nome):
    print(Fore.MAGENTA + f'\nTabuleiro da Almirante IA:\n{tabuleiro_ia.exibir_oculto()}')
    print(Fore.CYAN + f'\nTabuleiro do(a) Almirante {nome}:\n{tabuleiro_player.exibir_completo()}')

def solicitar_nome():
    animar_texto("Digite seu nome de comandante:", cor=Fore.CYAN)
    return input(Fore.WHITE + "Nome: ")

def exibir_menu():
    print(Fore.YELLOW + "\n=== MENU PRINCIPAL ===")
    print("1. Iniciar Jogo")
    print("2. Créditos")
    print("3. Alternar Som (Ativar/Desativar)")
    print("4. Sair")
    return input(Fore.WHITE + "Escolha uma opção: ")

def exibir_creditos():
    print(Fore.MAGENTA + "\n=== CRÉDITOS ===")
    print("Desenvolvido por: Goldero Informáticas")
    print("Projeto Batalha Naval em Python com IA, Sons e Interface Terminal.")
    input(Fore.WHITE + "\nPressione ENTER para voltar ao menu.")

def escolher_dificuldade():
    print(Fore.YELLOW + "\nEscolha a dificuldade:")
    print("1. Fácil")
    print("2. Médio")
    print("3. Difícil")
    while True:
        escolha = int(input(Fore.WHITE + "Opção (1-3): "))
        if escolha in [1, 2, 3]:
            return escolha
        else:
            print(Fore.RED + "Escolha inválida. Tente novamente.")