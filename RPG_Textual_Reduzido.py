#O tempo corre perigo, vc precisa restaurar o tempo para sua normalidade, achar o codigo para conseguir abrir um portal com senha
# para chegar no portal precisa de passar por 3 niveis, lagoa dos dragoes, berço de Kharzuth  e castelo de Drenvaar.

#O jogo é um RPG de aventura, onde o jogador deve explorar diferentes locais, resolver enigmas e enfrentar 
# inimigos para restaurar o tempo.

#O jogador deve coletar itens, interagir com personagens e tomar decisões que afetam o desenrolar da história.
#O jogo é dividido em três níveis, cada um com seu próprio conjunto de desafios e inimigos.

import random
import time
from classes_do_rpg import Personagem, NPC, Inimigo, Quest, escolher_classe, narrativa_inicio

# === CLASSE DO JOGADOR ===
local_atual = 1
itens_1 = {
    "Espada quebrada": {"ataque": 5, "durabilidade": 10},
    "Escudo de madeira": {"defesa": 3, "durabilidade": 15},
    "Poção de cura 1": {"cura": 10, "quantidade": 1},
    "katana enferrujada": {"ataque": 7, "durabilidade": 8},  
}  
itens = [
    ["Poções", "Poção de cura pequena", "Poção de cura média", "Poção de cura grande"],
    ["Armaduras", "Armadura de couro", "Armadura de ferro", "Armadura de mitril"],
    ["Armas", "Espada de madeira", "Espada de ferro", "Espada de mitril"]
]

itens_2 = {
    "Espada longa": {"ataque": 10, "durabilidade": 20},
    "Escudo de ferro": {"defesa": 4, "durabilidade": 20},
    "Poção de cura 2": {"cura": 20, "quantidade": 1},
    "katana afiada": {"ataque": 12, "durabilidade": 15},
}

itens_3 = {
    "Espada Sagrada": {"ataque": 15, "durabilidade": 30},
    "Escudo Forjado": {"defesa": 8, "durabilidade": 35},
    "Poção de cura 3": {"cura": 30, "quantidade": 1},
    "katana lendária": {"ataque": 20, "durabilidade": 25},
    "cajado do mago supremo": {"ataque": 15, "durabilidade": 28},
}

inventario = []

# Inimigos comuns
inimigos_aleatorios = [
    ("Goblin", 12, 3, 1, "veneno"),
    ("Esqueleto", 14, 4, 1, "furia"),
    ("Orc", 16, 5, 2, "furia"),
    ("Slime", 10, 2, 2, "cura"),
    ("Lobo Sangrento", 15, 4, 1, "furia"),
    ("Espectro", 12, 3, 3, "veneno"),
    ("Morto-vivo", 14, 4, 2, "cura"),
    ("Minotauro", 18, 6, 1, "furia"),
]

# Bosses
bosses = {
    "Dragão Ancião": (30, 7, 4, "furia"),
    "Kharzuth - Criador dos Dragões": (35, 8, 5, "cura"),
    "Drenvaar - Senhor do Tempo": (40, 9, 6, "veneno"),
}

# === FALAS NPCS ===
def condicao_coletar_3_baus(jogador):
    return jogador.contador_de_baus >= 3

def recompensa_moedas_50(jogador):
    jogador.ouro += 50
   

# ==== Instância de Quest e NPC ==== 
def visitar_npc(jogador):
    global local_atual
    if local_atual==1:
     npc_fase1.oferecer_quest(jogador)
    elif local_atual==2:
     npc_fase2.oferecer_quest(jogador)
    elif local_atual==3:
        npc_fase3.oferecer_quest(jogador)

def nova_quest_baus():
    return Quest(
        id='baus_1',
        titulo='Caçador de Baús',
        descricao='Encontre 3 baús misteriosos na Lagoa dos Dragões.',
        condicao_conclusao=condicao_coletar_3_baus,
        recompensa=recompensa_moedas_50
    )

quest_baus = Quest(
    id='baus_1',
    titulo='Caçador de Baús',
    descricao='Encontre 3 baús misteriosos na Lagoa dos Dragões.',
    condicao_conclusao=condicao_coletar_3_baus,
    recompensa=recompensa_moedas_50
)

npc_fase1 = NPC(
    nome='Samurai Aposentado',
    dialogo=[
        'Ah, jovem aventureiro…',
        'Preciso que você recupere 3 baús perdidos.',
        'Eles estão espalhados pela Lagoa dos Dragões.'
    ],
    quest=quest_baus
)

npc_fase2= NPC(
    nome='Dio Cavalheiro Esquecido',
    dialogo=[
        'Ah, jovem aventureiro…',
        'Preciso que você recupere 3 baús perdidos.',
        'Eles estão espalhados pela Lagoa dos Dragões.'
    ],
    quest=quest_baus
)

npc_fase3 = NPC(
    nome='Neo Necromante do Tempo',
    dialogo=[
        'Ah, jovem aventureiro…',
        'Preciso que você recupere 3 baús perdidos.',
        'Eles estão espalhados pela Lagoa dos Dragões.'
    ],
    quest=quest_baus
)
# === COMANDOS ===

def input_comandos(texto, jogador):
    while True:
        entrada = input(texto).lower().strip()

        if entrada in ["/inventario", "/inventário"]:
            jogador.mostrar_inventario()
        elif entrada == "/atributos":
            print(f"\nAtributos de {jogador.nome}:")
            print(f"Força: {jogador.forca_total()}")
            print(f"Defesa: {jogador.defesa_total()}")
            print(f"Vida: {jogador.vida}/{jogador.vida_maxima}")
            print(f"XP: {jogador.xp} | Nível: {jogador.nivel}")
            print(f"Ouro: {jogador.ouro}\n")
            print(f"Pontos de Atributos: {jogador.pontos}")
            upar = input("Deseja upar algum atributo? (s/n): ").lower().strip()
            if upar in ["s", "sim"]:
                jogador.upar_atributos()
            else:
                print("Ok, voltando ao jogo.")
        elif entrada == "/sair":
            print("Você decidiu sair do jogo. Até a próxima aventura!")
            exit()
        elif entrada in ["/ajuda", "/help"]:
            print("\nComandos disponíveis:")
            print("/inventario ou /inventário - Mostra o inventário do jogador.")
            print("/atributos - Mostra os atributos do jogador.")
            print("/ajuda ou /help - Mostra esta mensagem de ajuda.")
            print("/sair - Encerra o jogo.\n")
        else:
            return entrada
    

# === GAME OVER ===
def game_over(jogador):
    if jogador.esta_vivo():
      return
    tente_novamente = input("Você foi derrotado, deseja tentar novamente? (s/n): ").lower().strip()
    while tente_novamente not in ["s", "sim", "não", "n", "nao"]:
        print("Erro informe novamente: ")
        tente_novamente = input("Você foi derrotado, deseja tentar novamente? (s/n): ").lower().strip()
    if tente_novamente in ["s", "sim"]:
        print("Você decidiu tentar novamente. Boa sorte na sua jornada!")
        jogar()
    elif tente_novamente in ["não", "n", "nao"]:
        print("Você decidiu não tentar novamente. Muito obrigado por jogar! ")

# === FUNÇÕES DE BATALHA E VENDEDOR ===

def batalha(jogador, inimigo):
    global local_atual
    while jogador.esta_vivo() and inimigo.esta_vivo():
        jogador.habilidade_ativa(inimigo)
        inimigo.habilidade_ativa(jogador)
        jogador.veneno()
        inimigo.veneno()
        print(f"\n{jogador.nome} vs {inimigo.nome}")
        print(f"{jogador.nome}: {jogador.vida} de vida | {inimigo.nome}: {inimigo.vida} de vida")
        escolha_battle = input_comandos("""Escolha sua ação: 
Atacar(1):
Esquiva(2):
Usar poção de vida(3):""", jogador)
        if escolha_battle in ["1", "atacar"]:
            jogador.atacar(inimigo)
            if inimigo.esta_vivo():
                inimigo.atacar(jogador)
        elif escolha_battle in ["2", "desviar"]:
            esquiva = random.random()
            if esquiva < 0.5:
                print("Esquiva efetuada com sucesso")
            else:
                print("Esquiva falhou! Você tomou dano!")
                inimigo.atacar(jogador)
        elif escolha_battle in ["3", "usar poção de vida"]:
            jogador.curar(30)
        print(f"{jogador.nome}: {jogador.vida} de vida | {inimigo.nome}: {inimigo.vida} de vida")
        input("Pressione Enter para o próximo turno...\n")
    
    if jogador.esta_vivo():
        print(f"\nVocê derrotou {inimigo.nome}!\n")
        jogador.ganhar_xp(10)
        
    else:
        print(f"\nVocê foi derrotado por {inimigo.nome}...\n")
        game_over(jogador)


def vendedor(jogador):
    global local_atual
    chance = random.random()
    if chance < 0.4:
        print("\nVocê encontrou um vendedor!")
        print("Itens à venda:")
        print("[1] Espada de madeira - 10 Moedas")
        print("[2] Escudo de madeira - 10 Moedas")
        print("[3] Poção de cura pequena - 15 Moedas")
        escolha = input(f"Você tem {jogador.ouro} moedas. Deseja comprar algo? (s/n): ").lower().strip()
        while escolha not in ["s", "sim", "não", "n", "nao"]:
            print("Erro informe novamente: ")
            escolha = input("Quer comprar algo? (s/n): ").lower().strip()
        if escolha in ["s", "sim"]:
            while True:
                item = input("Qual item você deseja comprar? (1/2/3): ")
                if item == "1":
                    if jogador.ouro >= 10:
                        jogador.ouro -= 10
                        jogador.inventario[0].append({"nome": "Espada de madeira", **itens_1["Espada quebrada"]})
                        print("Você comprou uma Espada de madeira!")
                    else:
                        print("Você não tem moedas suficientes!")
                elif item == "2":
                    if jogador.ouro >= 10:
                        jogador.ouro -= 10
                        jogador.inventario[1].append({"nome": "Escudo de madeira", **itens_1["Escudo de madeira"]})
                        print("Você comprou um Escudo de madeira!")
                    else:
                        print("Você não tem moedas suficientes!")
                elif item == "3":
                    if jogador.ouro >= 15:
                        jogador.ouro -= 15
                        jogador.inventario[2].append({"nome": "Poção de cura pequena", **itens_1["Poção de cura 1"]})
                        print("Você comprou uma Poção de cura pequena!")
                    else:
                        print("Você não tem moedas suficientes!")
                else:
                    print("Item inválido.")
                novamente = input("Deseja comprar mais algo? (s/n): ").lower().strip()
                if novamente not in ["s", "sim"]:
                    break
        else:
            print("Ok, nos vemos em uma próxima aventura.\n")

def deseja_ir_para_proximo_mapa():
    resposta = input("Deseja ir para o próximo mapa? (s/n): ").strip().lower()
    return resposta not in ["não", "n", "nao"]

def evento_aleatorio(jogador, itens_fase):
    evento = random.choices(
        ["nada", "bau", "inimigo", "vendedor", "npc"],
        weights=[10, 25, 5, 15, 15],
        k=1
    )[0]

    if evento == "inimigo":
        inimigo_info = random.choice(inimigos_aleatorios)
        inimigo = Inimigo(*inimigo_info)
        print(f"\nVocê foi surpreendido por um {inimigo.nome}!")
        batalha(jogador, inimigo)
        if not jogador.esta_vivo():
            return False

    elif evento == "bau":
        print("Você encontrou um baú misterioso!")
        item_nome = random.choice(list(itens_fase.keys()))
        item = {"nome": item_nome, **itens_fase[item_nome]}
        if "ataque" in item:
            jogador.inventario[0].append(item)
        elif "defesa" in item:
            jogador.inventario[1].append(item)
        elif "cura" in item:
            jogador.inventario[2].append(item)
        print(f"Você encontrou: {item_nome}\n")
        jogador.contador_de_baus += 1

    elif evento == "vendedor":
        vendedor(jogador)

    elif evento == "npc":
        visitar_npc(jogador)

    else:
        print("Você não encontrou nada... só vento e silêncio.")

    return True

def explorar(jogador, local, itens_fase, nome_area):
    print(f"\nVocê chegou em {nome_area}!")
    while jogador.esta_vivo():
        resposta = input_comandos("Deseja explorar esta área? (s/n): ", jogador).lower().strip()
        if resposta not in ["s", "sim"]:
            print("Você decidiu parar de explorar esta área.")
            break
        print(f"Você começou a explorar {nome_area}...")
        time.sleep(1.5)
        continuar = evento_aleatorio(jogador, itens_fase)
        if not continuar:
            break
        continuar_explorando = input_comandos("Deseja continuar explorando? (s/n): ", jogador).lower().strip()
        if continuar_explorando not in ["s", "sim"]:
            print("Você decidiu parar de explorar esta área.")
            break

def jogar():
    narrativa_inicio()
    jogador = escolher_classe()
    print(f"Bem-vindo, {jogador.nome}! Sua aventura começa agora.\n")

    fases = [
        (1, itens_1, "Lagoa dos Dragões", "Dragão Ancião", (30, 10, 5, "furia")),
        (2, itens_2, "Berço de Kharzuth", "Kharzuth - Criador dos Dragões", (40, 12, 7, "cura")),
        (3, itens_3, "Castelo de Drenvaar", "Drenvaar - Senhor do Tempo", (50, 15, 9, "veneno")),
    ]

    for idx, (local, itens_fase, nome_area, boss_nome, boss_stats) in enumerate(fases, 1):
        print(f"\n{'='*30}\nFase {idx}: {nome_area}\n{'='*30}")
        explorar(jogador, local, itens_fase, nome_area)
        if not jogador.esta_vivo():
            return
        # Boss da fase
        print(f"\nVocê encontrou o boss: {boss_nome}!")
        boss = Inimigo(boss_nome, *boss_stats)
        batalha(jogador, boss)
        if not jogador.esta_vivo():
            return
        print(f"Parabéns! Você derrotou {boss_nome} e pode avançar para a próxima área!")
        jogador.contador_de_baus = 0  # Reseta para próxima fase (opcional)

    print("Você atravessou o portal do tempo e chegou em ???")
    print("Você não sabe onde está, mas sente que é o fim de sua jornada.")
    jogador.contador_de_baus = 0  # Reseta para o evento do portal
    while True:
        escolha = input_comandos("Quer explorar a região? (s/n): ", jogador).lower().strip()
        if escolha not in ["s", "sim"]:
            break
        print("Você começou a explorar o desconhecido...\n")
        time.sleep(1.5)
        print("Você encontrou um baú misterioso!")
        conjunto = random.choice([itens_1, itens_2, itens_3])
        item_encontrado_nome = random.choice(list(conjunto.keys()))
        item_encontrado = {"nome": item_encontrado_nome, **conjunto[item_encontrado_nome]}
        if "ataque" in item_encontrado:
            jogador.inventario[0].append(item_encontrado)
        elif "defesa" in item_encontrado:
            jogador.inventario[1].append(item_encontrado)
        elif "cura" in item_encontrado:
            jogador.inventario[2].append(item_encontrado)
        print(f"Você encontrou: {item_encontrado_nome}\n")
        jogador.contador_de_baus += 1
        if jogador.contador_de_baus >= 3:
            print("Você encontrou um goblin que saiu de um portal, no meio da vastidão do fundo branco!!")
            print("Goblin chega sorrateiramente em você e pergunta:\nquer participar de um jogo de adivinhação?")
            escolhaGoblin = input_comandos("Quer participar do jogo de adivinhação? (s/n): ", jogador).lower().strip()
            while escolhaGoblin not in ["s", "sim", "n", "nao", "não"]:
                print("Erro, informe novamente: ")
                escolhaGoblin = input_comandos("Quer participar do jogo de adivinhação? (s/n): ", jogador).lower().strip()
            if escolhaGoblin in ["s", "sim"]:
                print("Você aceitou o desafio do goblin!")
                print("O goblin lhe faz 3 perguntas:")
                pergunta1 = input_comandos("Qual é a capital das Terras Neutras? ", jogador).lower().strip()
                if pergunta1 == "berço de kharzuth":
                    print("Parabéns! Você acertou a primeira pergunta!")
                    print("O goblin te dá 20 moedas!")
                    jogador.ouro += 20
                    print(f"Você agora tem {jogador.ouro} moedas.")
                else:
                    print("Resposta errada! O goblin te esfaqueia")
                    jogador.vida -= 10
                    print(f"Você perdeu 10 de vida. Vida atual: {jogador.vida}")
                    if jogador.vida <= 0:
                        print("Você morreu! Fim de jogo.")
                        return
                    else:
                        print("essa doeu nao é mesmo?")
                pergunta2 = input_comandos("Qual é o nome do criador dos dragões? ", jogador).lower().strip()
                if pergunta2 == "kharzuth":
                    print("Parabéns! Você acertou a segunda pergunta!")
                    print("O goblin te dá 20 moedas!")
                    jogador.ouro += 20
                    print(f"Você agora tem {jogador.ouro} moedas.")
                else:
                    print("Resposta errada! O goblin te esfaqueia")
                    jogador.vida -= 10
                    print(f"Você perdeu 10 de vida. Vida atual: {jogador.vida}")
                    if jogador.vida <= 0:
                        print("Você morreu! Fim de jogo.")
                        return
                    else:
                        print("essa doeu nao é mesmo?")
                pergunta3 = input_comandos("onde estamos? ", jogador).lower().strip()
                if pergunta3 in ["???", "nao sei", "não sei", "no tempo"]:
                    print("Parabéns! Você acertou a terceira pergunta!")
                    print("O goblin te dá 20 moedas!")
                    jogador.ouro += 20
                    print(f"Você agora tem {jogador.ouro} moedas.")
                    print("O goblin desaparece em um portal, deixando você sozinho no desconhecido.")
                else:
                    print("Resposta errada! O goblin te esfaqueia")
                    jogador.vida -= 10
                    print(f"Você perdeu 10 de vida. Vida atual: {jogador.vida}")
                    if jogador.vida <= 0:
                        print("Você morreu! Fim de jogo.")
                        return
                    else:
                        print("O goblin desaparece em um portal, deixando você sozinho no desconhecido.")
            break  # Sai do loop após o evento do goblin

    print("Obrigado por jogar! Você completou a aventura!")
    exit()

if __name__ == "__main__":
    jogar()
