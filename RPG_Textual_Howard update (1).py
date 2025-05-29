#O tempo corre perigo, vc precisa restaurar o tempo para sua normalidade, achar o codigo para conseguir abrir um portal com senha
# para chegar no portal precisa de passar por 3 niveis, lagoa dos dragoes, berço de Kharzuth  e castelo de Drenvaar.

#O jogo é um RPG de aventura, onde o jogador deve explorar diferentes locais, resolver enigmas e enfrentar 
# inimigos para restaurar o tempo.

#O jogador deve coletar itens, interagir com personagens e tomar decisões que afetam o desenrolar da história.
#O jogo é dividido em três níveis, cada um com seu próprio conjunto de desafios e inimigos.

import random
import time
from classes_do_rpg import Personagem, NPC, Inimigo, Quest, escolher_classe,narrativa_inicio

# === CLASSE DO JOGADOR ===
local_atual = 1
itens_1 = {
    "Espada quebrada": {"ataque": 5, "durabilidade": 10},
    "Escudo de madeira": {"defesa": 3, "durabilidade": 15},
    "Poção de cura 1": {"cura": 10, "quantidade": 1},
    "katana enferrujada": {"ataque": 7, "durabilidade": 8},    
}

itens_2 = {
    "Espada longa": {"ataque": 10, "durabilidade": 20},
    "Escudo de ferro": {"defesa": 5, "durabilidade": 25},
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

inimigos_aleatorios = [
    "Goblin", "Esqueleto", "Orc", "Slime", "Lobo Sangrento", "Espectro", "morto-vivo", "minotauro"
]

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
        escolha_battle = input("""Escolha sua ação: 
Atacar(1):
Esquiva(2):
Usar poção de vida(3):""")
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
                        jogador.inventario.append("Espada de madeira")
                        print("Você comprou uma Espada de madeira!")
                    else:
                        print("Você não tem moedas suficientes!")
                elif item == "2":
                    if jogador.ouro >= 10:
                        jogador.ouro -= 10
                        jogador.inventario.append("Escudo de madeira")
                        print("Você comprou um Escudo de madeira!")
                    else:
                        print("Você não tem moedas suficientes!")
                elif item == "3":
                    if jogador.ouro >= 15:
                        jogador.ouro -= 15
                        jogador.inventario.append("Poção de cura pequena")
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

def explorar(jogador):
    global local_atual
    global local_atual, npc_fase1, npc_fase2, npc_fase3

   # Resetar progresso ao mudar de mapa
    jogador.contador_de_baus = 0
    jogador.quests_ativas = []
    jogador.quests_concluidas = []

    eventos = ["inimigo", "bau", "npc", "nada", "vendedor"]
    evento = random.choices(eventos, weights=[0.3, 0.3, 0.2, 0.1, 0.1])[0]
    while True:
        if local_atual == 1:
        
        
            npc_fase1.quest = nova_quest_baus()
            print("Você está na lagoa dos dragões. Muitos dragões estão adormecidos por aqui.")
            print("Você deve encontrar certos dragões por aqui!!!")
            print("Para você prosseguir em sua jornada deve fazer uma quest em cada mapa para enfrentar o boss e prosseguir em sua jornada")
            escolha = input("Quer explorar a região? (s/n): ").lower().strip()
            while escolha not in ["s", "sim", "não", "n", "nao"]:
                print("Erro, informe novamente: ")
                escolha = input("Quer explorar a região? (s/n): ").lower().strip()
            if escolha in ["s", "sim"]:
                while escolha == "s":
                    print("Você começou a explorar a lagoa dos dragões...\n")
                    time.sleep(1.5)
                    visitar_npc(jogador)
                    vendedor(jogador)
                    if random.random() >= 0.15:
                        print("\nUm baú misterioso apareceu!")
                        item_encontrado = random.choice(list(itens_1.keys()))
                        inventario.append(item_encontrado)
                        print(f"Você encontrou: {item_encontrado}\n")
                        jogador.contador_de_baus += 1
                        if jogador.contador_de_baus < 3:
                            
                            #mandar ele pro dragao direto até então
                            
                            explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()

                            while explorar_quest not in ["s", "sim", "n", "nao", "não"]:
                                print("Erro, informe novamente.")
                                explorar_quest = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()

                            while explorar_quest in ["s", "sim"] and jogador.contador_de_baus < 3:
                                print("Você começou a explorar a lagoa dos dragões...\n")
                                time.sleep(1.5)

                                if random.randint(1, 5) == 1:
                                    print("Você encontrou um baú misterioso!")
                                    item_encontrado = random.choice(list(itens_1.keys()))
                                    inventario.append(item_encontrado)
                                    print(f"Você encontrou: {item_encontrado}\n")
                                    jogador.contador_de_baus += 1

                                    faltam = 3 - jogador.contador_de_baus
                                    if faltam > 0:
                                        print(f"Você encontrou um baú, faltando apenas {faltam} para completar a quest.")
                                    else:
                                        print("Você encontrou todos os baús!")
                                        break
                                else:
                                    print("Nada por aqui... só vento e decepção.")

                                explorar_quest = input("Quer continuar explorando? (s/n): ").lower().strip()
                                while explorar_quest not in ["s", "sim", "n", "nao", "não"]:
                                    print("Erro, informe novamente.")
                                    explorar_quest = input("Quer continuar explorando? (s/n): ").lower().strip()

                            if jogador.contador_de_baus < 3:
                                print("Você decidiu não explorar mais a lagoa dos dragões. Boa sorte na sua jornada!")
                                print("Você encontrou um Dragão Ancião!")
                                inimigo = Inimigo("Dragão Ancião", 15, 5, 2, "furia")
                                batalha(jogador, inimigo)
                                game_over(jogador)
                                if deseja_ir_para_proximo_mapa():
                                    local_atual += 1
                                    print("Você avançou para o próximo mapa!")
                                    return
                                else:
                                    print("Você decidiu permanecer neste mapa por enquanto.")


                        if jogador.contador_de_baus >= 3:
                            jogador.checar_quests()
                            print("Você ganhou 50 moedas!")
                            jogador.ouro += 50
                            print(f"Você agora tem {jogador.ouro} moedas.")
                            jogador.contador_de_baus -= 3
                            vendedor(jogador)
                            print("Você continuou andando até que......")
                        break
                    else:
                        print("Nada por aqui... só vento e decepção.")
                    escolha = input("Quer continuar explorando? (s/n): ").lower().strip()
                print("Você decidiu não explorar mais a lagoa dos dragões. Boa sorte na sua jornada!")
                print("Você encontrou um Dragão Ancião!")
                inimigo = Inimigo("Dragão Ancião", 15, 5, 2, "furia")
                batalha(jogador, inimigo)
                game_over(jogador)
                if deseja_ir_para_proximo_mapa():
                    local_atual += 1
                    print("Você avançou para o próximo mapa!")
                    return
                else:
                    print("Você decidiu permanecer neste mapa por enquanto.")
                    
            else:
                print("Você decidiu não explorar a lagoa dos dragões. Boa sorte na sua jornada!")
                visitar_npc(jogador)
                escolha = input("Quer explorar a região atrás dos baús (s/n): ").lower().strip()
                
                while escolha not in ["s", "sim", "não", "n", "nao"]:
                    print("Erro, informe novamente: ")
                    escolha = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()
                
                if escolha in ["s", "sim"]:
                    print("Você começou a explorar a lagoa dos dragões...\n")
                    time.sleep(1.5)
                    print("Você encontrou um baú misterioso!")
                    item_encontrado = random.choice(list(itens_1.keys()))
                    inventario.append(item_encontrado)
                    print(f"Você encontrou: {item_encontrado}\n")
                    jogador.contador_de_baus += 1
                    print("Você encontrou um baú, faltando apenas 2 para completar a quest")
                    
                    if jogador.contador_de_baus < 3:
                            
                            #mandar ele pro dragao direto até então
                            
                            explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()
                            
                            while explorar_quest not in ["s", "sim", "não", "n", "nao"]:
                                print("Erro, informe novamente: ")
                                explorar_quest = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()
                            
                            while explorar_quest in ["s", "sim"] and jogador.contador_de_baus < 3:
                                print("Você começou a explorar a lagoa dos dragões...\n")
                                time.sleep(1.5)
                                print("Você encontrou um baú misterioso!")
                                item_encontrado = random.choice(list(itens_1.keys()))
                                inventario.append(item_encontrado)
                                print(f"Você encontrou: {item_encontrado}\n")
                                jogador.contador_de_baus += 1
                                faltam = 3 - jogador.contador_de_baus
                                if faltam > 0:
                                    print(f"Você encontrou um baú, faltando apenas {faltam} para completar a quest")
                                    explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()
                                else:
                                    break
                            
                                
                    if jogador.contador_de_baus >= 3:
                        jogador.checar_quests()
                        print("Você ganhou 50 moedas!")
                        jogador.ouro += 50
                        print(f"Você agora tem {jogador.ouro} moedas.")
                        jogador.contador_de_baus -= 3
                        vendedor(jogador)
                        print("Você continuou andando até que......")
                    


                elif escolha in ["não", "n", "nao"]:
                    print("Você tem que fazer a quest para prosseguir em sua jornada")
                    escolha = input("Quer explorar a região atrás dos baús (s/n): ").lower().strip()
                    while escolha not in ["s", "sim", "não", "n", "nao"]:
                        print("Erro, informe novamente: ")
                        escolha = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()
                    if escolha in ["s", "sim"]:
                        print("Você começou a explorar a lagoa dos dragões...\n")
                        time.sleep(1.5)
                        print("Você encontrou um baú misterioso!")
                        item_encontrado = random.choice(list(itens_1.keys()))
                        inventario.append(item_encontrado)
                        print(f"Você encontrou: {item_encontrado}\n")
                        jogador.contador_de_baus += 1
                        print("Você encontrou um baú, faltando apenas 2 para completar a quest")
                        if jogador.contador_de_baus < 3:
                            
                            #mandar ele pro dragao direto até então
                            
                            explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()
                            while explorar_quest not in ["s", "sim", "não", "n", "nao"]:
                                print("Erro, informe novamente: ")
                                explorar_quest = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()
                            while explorar_quest in ["s", "sim"] and jogador.contador_de_baus < 3:
                                print("Você começou a explorar a lagoa dos dragões...\n")
                                time.sleep(1.5)
                                print("Você encontrou um baú misterioso!")
                                item_encontrado = random.choice(list(itens_1.keys()))
                                inventario.append(item_encontrado)
                                print(f"Você encontrou: {item_encontrado}\n")
                                jogador.contador_de_baus += 1
                                faltam = 3 - jogador.contador_de_baus
                                if faltam > 0:
                                    print(f"Você encontrou um baú, faltando apenas {faltam} para completar a quest")
                                    explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()
                                else:
                                    break
                            
                                
                    if jogador.contador_de_baus >= 3:
                        jogador.checar_quests()
                        print("Você ganhou 50 moedas!")
                        jogador.ouro += 50
                        print(f"Você agora tem {jogador.ouro} moedas.")
                        jogador.contador_de_baus -= 3
                        vendedor(jogador)
                        print("Você continuou andando até que......")
                    elif escolha in ["não", "n", "nao"]:
                        print("Você decidiu não explorar mais a lagoa dos dragões. Boa sorte na sua jornada!")
                        print("Você encontrou um Dragão Ancião!")
                        inimigo = Inimigo("Dragão Ancião", 100, 100, 100, "furia")
                        batalha(jogador, inimigo)
                        game_over(jogador)
                print("Você encontrou um Dragão Ancião!")
                inimigo = Inimigo("Dragão Ancião", 15, 5, 2, "furia")
                batalha(jogador, inimigo)
                game_over(jogador)
                if deseja_ir_para_proximo_mapa():
                    local_atual += 1
                    print("Você avançou para o próximo mapa!")
                    return
                else:
                    print("Você decidiu permanecer neste mapa por enquanto.")
            

        elif local_atual == 2:
            npc_fase2.quest = nova_quest_baus()
            evento = random.choice(["inimigo", "bau", "npc", "nada", "vendedor"])
            print("Você está no berço de Kharzuth. Aqui, os dragões são criados.")
            print("Você deve encontrar certa parte do código por aqui!!!")
            escolha = input("Quer explorar a região? (s/n): ").lower().strip()
            while escolha not in ["s", "sim", "não", "n", "nao"]:
                print("Erro, informe novamente: ")
                escolha = input("Quer explorar a região? (s/n): ").lower().strip()
            if escolha in ["s", "sim"]:
                while escolha == "s":
                    print("Você começou a explorar berço de Kharzuth...\n")
                    time.sleep(1.5)
                    visitar_npc(jogador)
                    vendedor(jogador)
                    if random.random() >= 0.15:
                        print("\nUm baú misterioso apareceu!")
                        item_encontrado = random.choice(list(itens_2.keys()))
                        inventario.append(item_encontrado)
                        print(f"Você encontrou: {item_encontrado}\n")
                        jogador.contador_de_baus += 1
                        if jogador.contador_de_baus < 3:
                            
                            #mandar ele pro Kharzuth direto até então
                            
                            explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()

                            while explorar_quest not in ["s", "sim", "n", "nao", "não"]:
                                print("Erro, informe novamente.")
                                explorar_quest = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()

                            while explorar_quest in ["s", "sim"] and jogador.contador_de_baus < 3:
                                print("Você começou a explorar o berço de Kharzuth...\n")
                                time.sleep(1.5)

                                if random.randint(1, 5) == 1:
                                    print("Você encontrou um baú misterioso!")
                                    item_encontrado = random.choice(list(itens_2.keys()))
                                    inventario.append(item_encontrado)
                                    print(f"Você encontrou: {item_encontrado}\n")
                                    jogador.contador_de_baus += 1

                                    faltam = 3 - jogador.contador_de_baus
                                    if faltam > 0:
                                        print(f"Você encontrou um baú, faltando apenas {faltam} para completar a quest.")
                                    else:
                                        print("Você encontrou todos os baús!")
                                        break
                                else:
                                    print("Nada por aqui... só vento e decepção.")

                                explorar_quest = input("Quer continuar explorando? (s/n): ").lower().strip()
                                while explorar_quest not in ["s", "sim", "n", "nao", "não"]:
                                    print("Erro, informe novamente.")
                                    explorar_quest = input("Quer continuar explorando? (s/n): ").lower().strip()
                                    

                            if jogador.contador_de_baus < 3:
                                print("Você decidiu não explorar mais o berço de Kharzuth. Boa sorte na sua jornada!")
                                print("Você encontrou Kharzuth - Criador dos Dragões!")
                                inimigo = Inimigo("Kharzuth - Criador dos Dragões", 20, 6, 3, "cura")
                                batalha(jogador, inimigo)
                                game_over(jogador)
                                if deseja_ir_para_proximo_mapa():
                                    local_atual += 1
                                    print("Você avançou para o próximo mapa!")
                                    return
                                else:
                                    print("Você decidiu permanecer neste mapa por enquanto.")


                        if jogador.contador_de_baus >= 3:
                            jogador.checar_quests()
                            print("Você ganhou 50 moedas!")
                            jogador.ouro += 50
                            print(f"Você agora tem {jogador.ouro} moedas.")
                            jogador.contador_de_baus -= 3
                            vendedor(jogador)
                            print("Você continuou andando até que......")
                        break
                    else:
                        print("Nada por aqui... só vento e decepção.")
                    escolha = input("Quer continuar explorando? (s/n): ").lower().strip()
                print("Você decidiu não explorar mais o berço de Kharzuth. Boa sorte na sua jornada!")
                print("Você encontrou Kharzuth - Criador dos Dragões!")
                inimigo = Inimigo("Kharzuth - Criador dos Dragões", 20, 6, 3, "cura")
                batalha(jogador, inimigo)
                game_over(jogador)
                if deseja_ir_para_proximo_mapa():
                    local_atual += 1
                    print("Você avançou para o próximo mapa!\n")
                    return
                else:
                    print("Você decidiu permanecer neste mapa por enquanto.")
            else:
                print("Você decidiu não explorar o berço de Kharzuth. Boa sorte na sua jornada!")
                visitar_npc(jogador)
                escolha = input("Quer explorar a região atrás dos baús (s/n): ").lower().strip()
                
                while escolha not in ["s", "sim", "não", "n", "nao"]:
                    print("Erro, informe novamente: ")
                    escolha = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()
                
                if escolha in ["s", "sim"]:
                    print("Você começou a explorar a berço de Kharzuth...\n")
                    time.sleep(1.5)
                    print("Você encontrou um baú misterioso!")
                    item_encontrado = random.choice(list(itens_2.keys()))
                    inventario.append(item_encontrado)
                    print(f"Você encontrou: {item_encontrado}\n")
                    jogador.contador_de_baus += 1
                    print("Você encontrou um baú, faltando apenas 2 para completar a quest")
                    
                    if jogador.contador_de_baus < 3:
                            
                            #mandar ele pro dragao direto até então
                            
                            explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()
                            
                            while explorar_quest not in ["s", "sim", "não", "n", "nao"]:
                                print("Erro, informe novamente: ")
                                explorar_quest = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()
                            
                            while explorar_quest in ["s", "sim"] and jogador.contador_de_baus < 3:
                                print("Você começou a explorar o berço de Kharzuth...\n")
                                time.sleep(1.5)
                                print("Você encontrou um baú misterioso!")
                                item_encontrado = random.choice(list(itens_2.keys()))
                                inventario.append(item_encontrado)
                                print(f"Você encontrou: {item_encontrado}\n")
                                jogador.contador_de_baus += 1
                                faltam = 3 - jogador.contador_de_baus
                                if faltam > 0:
                                    print(f"Você encontrou um baú, faltando apenas {faltam} para completar a quest")
                                    explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()
                                else:
                                    break
                            
                                
                    if jogador.contador_de_baus >= 3:
                            jogador.checar_quests()
                            print("Você ganhou 50 moedas!")
                            jogador.ouro += 50
                            print(f"Você agora tem {jogador.ouro} moedas.")
                            jogador.contador_de_baus -= 3
                            vendedor(jogador)
                            print("Você continuou andando até que......")
                        
                    


                elif escolha in ["não", "n", "nao"]:
                    print("Você tem que fazer a quest para prosseguir em sua jornada")
                    escolha = input("Quer explorar a região atrás dos baús (s/n): ").lower().strip()
                    while escolha not in ["s", "sim", "não", "n", "nao"]:
                        print("Erro, informe novamente: ")
                        escolha = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()
                    if escolha in ["s", "sim"]:
                        print("Você começou a explorar berço de Kharzuth...\n")
                        time.sleep(1.5)
                        print("Você encontrou um baú misterioso!")
                        item_encontrado = random.choice(list(itens_2.keys()))
                        inventario.append(item_encontrado)
                        print(f"Você encontrou: {item_encontrado}\n")
                        jogador.contador_de_baus += 1
                        print("Você encontrou um baú, faltando apenas 2 para completar a quest")
                        if jogador.contador_de_baus < 3:
                            
                            #mandar ele pro dragao direto até então
                            
                            explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()
                            while explorar_quest not in ["s", "sim", "não", "n", "nao"]:
                                print("Erro, informe novamente: ")
                                explorar_quest = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()
                            while explorar_quest in ["s", "sim"] and jogador.contador_de_baus < 3:
                                print("Você começou a explorar o berço de Kharzuth...\n")
                                time.sleep(1.5)
                                print("Você encontrou um baú misterioso!")
                                item_encontrado = random.choice(list(itens_2.keys()))
                                inventario.append(item_encontrado)
                                print(f"Você encontrou: {item_encontrado}\n")
                                jogador.contador_de_baus += 1
                                faltam = 3 - jogador.contador_de_baus
                                if faltam > 0:
                                    print(f"Você encontrou um baú, faltando apenas {faltam} para completar a quest")
                                    explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()
                                else:
                                    break
                            
                                
                    if jogador.contador_de_baus >= 3:
                            jogador.checar_quests()
                            print("Você ganhou 50 moedas!")
                            jogador.ouro += 50
                            print(f"Você agora tem {jogador.ouro} moedas.")
                            jogador.contador_de_baus -= 3
                            vendedor(jogador)
                            print("Você continuou andando até que......")
                    elif escolha in ["não", "n", "nao"]:
                        print("Você decidiu não explorar mais o berço de Kharzuth. Boa sorte na sua jornada!")
                        print("Você encontrou Kharzuth - Criador dos Dragões!")
                        inimigo = Inimigo("Kharzuth - Criador dos Dragões", 100, 100, 100, "furia")
                        batalha(jogador, inimigo)
                        game_over(jogador)
                print("Você encontrou Kharzuth - Criador dos Dragões!")
                inimigo = Inimigo("Kharzuth - Criador dos Dragões", 20, 6, 3, "cura")
                batalha(jogador, inimigo)
                game_over(jogador)
                if deseja_ir_para_proximo_mapa():
                    local_atual += 1
                    print("Você avançou para o próximo mapa!\n")
                    return
                else:
                    print("Você decidiu permanecer neste mapa por enquanto.")
        

        elif local_atual == 3: 
            npc_fase3.quest = nova_quest_baus()
            print("Você está no castelo de Drenvaar. Aqui, o Senhor do Tempo reside.")
            print("Você deve encontrar certa parte do código por aqui!!!")
            escolha = input("Quer explorar a região? (s/n): ").lower().strip()
            while escolha not in ["s", "sim", "não", "n", "nao"]:
                print("Erro, informe novamente: ")
                escolha = input("Quer explorar a região? (s/n): ").lower().strip()
            if escolha in ["s", "sim"]:
                while escolha == "s":
                    print("Você começou a explorar o castelo de Drenvaar...")
                    time.sleep(1.5)
                    visitar_npc(jogador)
                    vendedor(jogador)
                    if random.random() >= 0.15:
                        print("\nUm baú misterioso apareceu!")
                        item_encontrado = random.choice(list(itens_3.keys()))
                        inventario.append(item_encontrado)
                        print(f"Você encontrou: {item_encontrado}\n")
                        jogador.contador_de_baus += 1
                        if jogador.contador_de_baus < 3:
                            #mandar ele pro Drenvaar direto até então
                            
                            explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()

                            while explorar_quest not in ["s", "sim", "n", "nao", "não"]:
                                print("Erro, informe novamente: ")
                                explorar_quest = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()
                            while explorar_quest in ["s", "sim"] and jogador.contador_de_baus <3:
                                print("Você começou a explorar o Castelo de Drenvaar...\n")
                                time.sleep(1.5)
                                print("Você encontrou um baú misterioso!")
                                item_encontrado = random.choice(list(itens_3.keys()))
                                inventario.append(item_encontrado)
                                print(f"Você encontrou: {item_encontrado}\n")
                                jogador.contador_de_baus += 1
                                faltam = 3 - jogador.contador_de_baus
                                if faltam > 0:
                                    print(f"Você encontrou um baú, faltando apenas {faltam} para completar a quest")
                                    explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()
                                else:
                                    break
                        if jogador.contador_de_baus >= 3:
                            jogador.checar_quests()
                            print("Você ganhou 50 moedas!")
                            jogador.ouro += 50
                            print(f"Você agora tem {jogador.ouro} moedas.")
                            vendedor(jogador)
                            print("Você continuou andando até que......") 
                            escolha="s"
                        elif escolha in ["não", "n", "nao"]:
                            print("Você decidiu não explorar mais o Castelo de Drenvaar. Boa sorte na sua jornada!")
                            print("Você encontrou o Drenvaar - Senhor do Tempo!")
                            inimigo = Inimigo("Drenvaar - Senhor do Tempo", 100, 100, 100, "furia")
                            batalha(jogador, inimigo)
                            game_over(jogador)
                            print("Parabéns! Você derrotou o Senhor do Tempo e restaurou o fluxo temporal!")
                            print("FIM DE JOGO. Muito obrigado por jogar!")
                            deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()
                            while deseja_jogar_novamente not in ["s", "sim", "n", "nao", "não"]:
                                print("Erro, informe novamente: ")
                                deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()
                            if deseja_jogar_novamente in ["s", "sim"]:
                             print("Reiniciando o jogo...")
                             time.sleep(2)
                             jogar()
                            elif deseja_jogar_novamente in ["n", "não", "nao"]:
                             print("Obrigado por jogar! Até a próxima!")
                             break
                            while deseja_jogar_novamente not in ["s", "sim", "n", "nao", "não"]:
                             print("Erro, informe novamente: ")
                             deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()
                            
                    escolha = input("Quer continuar explorando? (s/n): ").lower().strip()
                print("Você decidiu não explorar mais o castelo de Drenvaar. Boa sorte na sua jornada!")
                print("Você encontrou Drenvaar - Senhor do Tempo!")
                inimigo = Inimigo("Drenvaar - Senhor do Tempo", 25, 7, 4, "veneno")
                batalha(jogador, inimigo)
                game_over(jogador)
                print("Parabéns! Você derrotou o Senhor do Tempo e restaurou o fluxo temporal!")
                print("FIM DE JOGO. Muito obrigado por jogar!")
                deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()
                while deseja_jogar_novamente not in ["s", "sim", "n", "nao", "não"]:
                 print("Erro, informe novamente: ")
                 deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()
                if deseja_jogar_novamente in ["s", "sim"]:
                 print("Reiniciando o jogo...")
                 time.sleep(2)
                 jogar()
                elif deseja_jogar_novamente in ["n", "não", "nao"]:
                  print("Obrigado por jogar! Até a próxima!")
                  exit()
                while deseja_jogar_novamente not in ["s", "sim", "n", "nao", "não"]:
                 print("Erro, informe novamente: ")
                 deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()
            else:
                print("Você decidiu não explorar o castelo de Drenvaar. Boa sorte na sua jornada!")
                visitar_npc(jogador)
                escolha = input("Quer explorar a região atrás dos baús (s/n): ").lower().strip()
                while escolha not in ["s", "sim", "não", "n", "nao"]:
                    print("Erro, informe novamente: ")
                    escolha = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()
                if escolha in ["s", "sim"]:
                    print("Você começou a explorar a lagoa dos dragões...\n")
                    time.sleep(1.5)
                    print("Você encontrou um baú misterioso!")
                    item_encontrado = random.choice(list(itens_3.keys()))
                    inventario.append(item_encontrado)
                    print(f"Você encontrou: {item_encontrado}\n")
                    jogador.contador_de_baus += 1
                    print("Você encontrou um baú, faltando apenas 2 para completar a quest")
                if jogador.contador_de_baus >= 3:
                            
                            #mandar ele pro BOSS direto até então
                            
                            explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()
                            
                            while explorar_quest not in ["s", "sim", "não", "n", "nao"]:
                                print("Erro, informe novamente: ")
                                explorar_quest = input("Quer explorar a região atrás dos baús? (s/n): ").lower().strip()
                            
                            while explorar_quest in ["s", "sim"] and jogador.contador_de_baus <3:
                                print("Você começou a explorar o Castelo de Drenvaar...\n")
                                time.sleep(1.5)
                                print("Você encontrou um baú misterioso!")
                                item_encontrado = random.choice(list(itens_3.keys()))
                                inventario.append(item_encontrado)
                                print(f"Você encontrou: {item_encontrado}\n")
                                jogador.contador_de_baus += 1
                                faltam = 3 - jogador.contador_de_baus
                                if faltam > 0:
                                    print(f"Você encontrou um baú, faltando apenas {faltam} para completar a quest")
                                    explorar_quest = input("Você quer explorar para achar os restantes dos baús? (s/n): ").lower().strip()
                                else:
                                    break
                            if jogador.contador_de_baus >= 3:
                                jogador.checar_quests()
                                print("Você ganhou 50 moedas!")
                                jogador.ouro += 50
                                print(f"Você agora tem {jogador.ouro} moedas.")
                                vendedor(jogador)
                                print("Você continuou andando até que......")
                                escolha="s"
                elif escolha in ["não", "n", "nao"]:
                    print("Você decidiu não explorar mais o Castelo de Drenvaar. Boa sorte na sua jornada!")
                    print("Você encontrou o Drenvaar - O Senhor do Tempo!")
                    inimigo = Inimigo("Drenvaar - O Senhor do Tempo", 100, 100, 100, "furia")
                    batalha(jogador, inimigo)
                    game_over(jogador)
                    print("Parabéns! Você derrotou o Senhor do Tempo e restaurou o fluxo temporal!")
                    print("FIM DE JOGO. Muito obrigado por jogar!")
                    deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()
                    while deseja_jogar_novamente not in ["s", "sim", "n", "nao", "não"]:
                     print("Erro, informe novamente: ")
                     deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()
                    if deseja_jogar_novamente in ["s", "sim"]:
                     print("Reiniciando o jogo...")
                     time.sleep(2)
                     jogar()
                    elif deseja_jogar_novamente in ["n", "não", "nao"]:
                      print("Obrigado por jogar! Até a próxima!")
                      exit()
                    while deseja_jogar_novamente not in ["s", "sim", "n", "nao", "não"]:
                     print("Erro, informe novamente: ")
                     deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()
                   
                    
                    
                print("Você encontrou Drenvaar - Senhor do Tempo!")
                inimigo = Inimigo("Drenvaar - Senhor do Tempo", 25, 7, 4, "veneno")
                batalha(jogador, inimigo)
                game_over(jogador)
                print("Parabéns! Você derrotou o Senhor do Tempo e restaurou o fluxo temporal!")
                print("FIM DE JOGO. Muito obrigado por jogar!")
                deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()
                while deseja_jogar_novamente not in ["s", "sim", "n", "nao", "não"]:
                 print("Erro, informe novamente: ")
                 deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()
                if deseja_jogar_novamente in ["s", "sim"]:
                 print("Reiniciando o jogo...")
                 time.sleep(2)
                 jogar()
                elif deseja_jogar_novamente in ["n", "não", "nao"]:
                 print("Obrigado por jogar! Até a próxima!")
                 exit()
                while deseja_jogar_novamente not in ["s", "sim", "n", "nao", "não"]:
                 print("Erro, informe novamente: ")
                 deseja_jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower().strip()          
        else:
            if evento == "bau":
                print("Você encontrou um baú escondido!")
                recompensa = random.choice(["ouro", "item", "poção"])
                if recompensa == "ouro":
                    ganho = random.randint(10, 50)
                    jogador.ouro += ganho
                    print(f"Você encontrou {ganho} moedas no baú!")
                elif recompensa == "item":
                    item = random.choice(["Adaga Rústica", "Elmo de Couro"])
                    jogador.inventario.append(item)
                    print(f"Você encontrou um item raro: {item}!")
                elif recompensa == "poção":
                    jogador.inventario.append("Poção de cura pequena")
                    print("Você encontrou uma Poção de cura pequena!")
                jogador.contador_de_baus += 1
            elif evento == "npc":
                print("Você encontrou um viajante misterioso...")
                visitar_npc(jogador)
            elif evento == "vendedor":
                vendedor(jogador)
            else:
                print("Você caminhou por um tempo, mas não encontrou nada além de silêncio e vento...")

   

# === LOOP PRINCIPAL ===
def jogar():
    global local_atual
    local_atual = 1
    narrativa_inicio()
    jogador = escolher_classe()
    while jogador.esta_vivo():
        explorar(jogador)

# === INICIO ===
if __name__ == "__main__": 
    jogar()
