import random
import time

gold = 0
vida = 0
mana = 0

atributos = {
    "vitalidade": 1,
    "mente": 1,
    "resistencia": 1,
    "forca": 1,
    "destreza": 1,
    "inteligencia": 1,
    "fé": 1,
    "arcano": 1
}

def character():
    print("Bem-vindo ao jogo de RPG!")
    time.sleep(1)
    nome = input("Qual é o seu nome, aventureiro?\n")
    print(f"Olá, {nome}!")
    classe = escolher_classe()
    aplicar_atributos(classe)
    mapas(classe)

def escolher_classe():
    while True:
        classe = input("Escolha sua classe (guerreiro/mago/arqueiro): ").lower().strip()
        if classe in ["guerreiro", "mago", "arqueiro"]:
            return classe
        print("Classe inválida!")

def aplicar_atributos(classe):
    global vida, mana
    if classe == "guerreiro":
        atributos.update(forca=7, destreza=3, fé=3, vitalidade=6, resistencia=6)
    elif classe == "mago":
        atributos.update(inteligencia=7, mente=6, arcano=6, fé=3, destreza=3)
    elif classe == "arqueiro":
        atributos.update(destreza=7, forca=3, mente=6, arcano=6, fé=3)
    vida = (atributos["vitalidade"] + atributos["resistencia"]) * 10
    mana = ((atributos["inteligencia"] + atributos["fé"] + atributos["arcano"] + atributos["mente"]) / 4) * 10
    print(f"Vida: {vida:.0f}, Mana: {mana:.0f}")

def mapas(classe):
    mapas = [
        "floresta inicial",
        "montanhas gélidas",
        "deserto ardente",
        "pântano sombrio",
        "castelo amaldiçoado",
        "vulcão dos dragões"
    ]
    for i, nome in enumerate(mapas, 1):
        print(f"\n--- Mapa {i}: {nome.title()} ---")
        time.sleep(1)
        explorar_mapa(i, classe)
        if vida <= 0:
            print("Você morreu! Fim de jogo.")
            return
    print(f"\nFim da jornada! Ouro: {gold}, Vida: {vida:.0f}")

def explorar_mapa(nivel, classe):
    chance_encontro = random.random()
    if chance_encontro < 0.7:
        grupo = gerar_inimigos_por_nivel(nivel)
        for inimigo in grupo:
            batalha(inimigo)
            if vida <= 0:
                break
    else:
        print("Você explorou sem encontrar inimigos.")

def gerar_inimigos_por_nivel(nivel):
    fracos = ["Goblin", "Lobo", "Esqueleto"]
    medios = ["Orc", "Zumbi"]
    fortes = ["Grifo", "Rei Goblin"]
    chefes = ["Dragão", "Guardião Elemental"]

    grupo = []

    if nivel <= 2:
        grupo = random.choices(fracos, k=random.randint(1, 3))
    elif nivel <= 4:
        grupo = random.choices(fracos + medios, k=random.randint(1, 2))
        if random.random() < 0.3:
            grupo.append(random.choice(medios))
    else:
        grupo = [random.choice(medios + fortes)]
        if random.random() < 0.5:
            grupo.append(random.choice(fortes + chefes))
    return grupo

def batalha(inimigo):
    global vida, gold
    inimigos_stats = {
        "Goblin": (10, 2), "Lobo": (12, 3), "Esqueleto": (15, 3),
        "Orc": (20, 4), "Zumbi": (18, 4), "Grifo": (25, 6),
        "Rei Goblin": (35, 6), "Dragão": (50, 8), "Guardião Elemental": (60, 9)
    }

    hp, atk = inimigos_stats.get(inimigo, (10, 2))
    print(f"\n⚔️ Encontro: {inimigo} apareceu com {hp} de vida e {atk} de força!")

    if inimigo == "Goblin":
        batalha_goblin_quiz(hp, atk)
    else:
        batalha_combate(hp, atk, inimigo)

def batalha_goblin_quiz(hp, atk):
    global vida, gold
    pergunta = quest()
    print(f"Goblin: {pergunta}")
    resposta = input("Sua resposta: ").strip().lower()

    corretas = {
        "a lua é feita de queijo? (sim/não)": "não",
        "você já matou um goblin antes? (sim/não)": "sim",
        "a capital da frança é paris? (sim/não)": "sim",
        "dragões cospem fogo ou água?": "fogo",
        "o que é maior: um castelo ou um cogumelo gigante?": "um castelo",
        "2 + 2 é igual a 5? (sim/não)": "não",
        "você é mais rápido que um grifo? (sim/não)": "não",
        "o sol nasce no leste? (sim/não)": "sim",
        "elfos têm orelhas pontudas? (sim/não)": "sim",
        "você consegue falar goblinês fluente? (sim/não)": "não"
    }

    if resposta == corretas.get(pergunta.lower().strip(), ""):
        ganho = random.randint(30, 80)
        gold += ganho
        print(f"✅ Resposta correta! Você ganhou {ganho} de ouro.")
    else:
        vida -= atk
        print(f"❌ Errado! Você levou {atk} de dano. Vida atual: {vida:.0f}")

def batalha_combate(hp, atk, inimigo):
    global vida, gold
    forca_jogador = atributos.get("forca", 5)
    while hp > 0 and vida > 0:
        dano = random.randint(forca_jogador - 1, forca_jogador + 3)
        hp -= dano
        print(f"💥 Você atacou e causou {dano} de dano! Vida do {inimigo}: {max(hp, 0)}")
        time.sleep(0.5)

        if hp > 0:
            vida -= atk
            print(f"⚠️ {inimigo} contra-atacou e causou {atk} de dano! Sua vida: {max(vida, 0)}")
            time.sleep(0.5)

    if vida > 0:
        ganho = random.randint(20, 100)
        gold += ganho
        print(f"🏆 Você derrotou {inimigo} e ganhou {ganho} de ouro!")

def quest():
    perguntas = [
        "A lua é feita de queijo? (sim/não)",
        "Você já matou um goblin antes? (sim/não)",
        "A capital da França é Paris? (sim/não)",
        "Dragões cospem fogo ou água?",
        "O que é maior: um castelo ou um cogumelo gigante?",
        "2 + 2 é igual a 5? (sim/não)",
        "Você é mais rápido que um grifo? (sim/não)",
        "O sol nasce no leste? (sim/não)",
        "Elfos têm orelhas pontudas? (sim/não)",
        "Você consegue falar goblinês fluente? (sim/não)"
    ]
    return random.choice(perguntas)

# Início do jogo
character()
