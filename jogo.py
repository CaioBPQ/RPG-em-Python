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

def itens():
    return {
        "Espada": 10,
        "Espada Lendária": 20,
        "Armadura": 15,
        "Armadura Mística": 25,
        "Poção de Vida": 20,
        "Poção de Mana": 20,
        "Escudo": 25,
        "Arco": 30
    }

def loot():
    global gold, vida, mana
    todos_itens = itens()
    bau = random.randint(1, 100)
    
    if bau <= 50:
        print("Você encontrou um baú vazio!")
    elif 50 < bau <= 80:
        ouro = random.randint(10, 50)
        print(f"Você encontrou {ouro} de ouro!")
        gold += ouro
    elif 80 < bau <= 95:
        item = random.choice(["Espada", "Armadura", "Poção de Mana"])
        print(f"Você encontrou um(a) {item}!")
        aplicar_item(item, todos_itens)
    else:
        item = random.choice(["Espada Lendária", "Armadura Mística", "Poção de Vida"])
        print(f"Você encontrou um(a) {item} raro(a)!")
        gold += 100
        aplicar_item(item, todos_itens)

def aplicar_item(item, todos_itens):
    global vida, mana
    bonus = todos_itens.get(item, 0)
    
    if "Espada" in item or item == "Arco":
        atributos["forca"] += bonus // 10
        print(f"⚔️ Sua força aumentou em {bonus // 10}!")
    elif "Armadura" in item or item == "Escudo":
        atributos["resistencia"] += bonus // 10
        print(f"🛡️ Sua resistência aumentou em {bonus // 10}!")
    elif item == "Poção de Vida":
        vida += bonus
        print(f"❤️ Sua vida aumentou em {bonus}!")
    elif item == "Poção de Mana":
        mana += bonus
        print(f"💧 Sua mana aumentou em {bonus}!")

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
    chance = random.random()
    if chance < 0.6:
        grupo = gerar_inimigos_por_nivel(nivel)
        for inimigo in grupo:
            batalha(inimigo)
            if vida <= 0:
                break
    elif chance < 0.9:
        print("Você encontrou um baú misterioso...")
        loot()  # chama o sistema de loot
    else:
        print("Você explorou sem encontrar nada.")

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
    global vida, mana, gold
    defesa_ativa = False
    forca_jogador = atributos.get("forca", 5)

    while hp > 0 and vida > 0:
        print(f"\n👊 {inimigo} - Vida: {hp} | 🧍 Você - Vida: {vida:.0f}, Mana: {mana:.0f}")
        print("O que deseja fazer?")
        print("1 - Atacar")
        print("2 - Usar Poção de Vida (20 de cura, 10 de mana)")
        print("3 - Defender (reduz dano pela metade no próximo ataque)")

        acao = input("Escolha sua ação (1/2/3): ").strip()

        if acao == "1":
            dano = random.randint(forca_jogador - 1, forca_jogador + 2)
            hp -= dano
            print(f"💥 Você atacou e causou {dano} de dano!")

        elif acao == "2":
            if mana >= 10:
                cura = 20
                vida += cura
                mana -= 10
                print(f"🧪 Você usou uma Poção de Vida. +{cura} vida, -10 mana.")
            else:
                print("⚠️ Mana insuficiente para usar poção!")

        elif acao == "3":
            defesa_ativa = True
            print("🛡️ Você se prepara para se defender!")
        else:
            print("❌ Ação inválida! Você perdeu o turno.")

        # Inimigo ataca (se ainda estiver vivo)
        if hp > 0:
            dano_recebido = atk // 2 if defesa_ativa else atk
            vida -= dano_recebido
            print(f"⚔️ O {inimigo} atacou e causou {dano_recebido} de dano!")
            defesa_ativa = False  # zera após um uso

        time.sleep(0.5)

    if vida > 0:
        ganho = random.randint(20, 60)
        gold += ganho
        print(f"\n🏆 Você derrotou o {inimigo} e ganhou {ganho} de ouro!")
    else:
        print(f"\n💀 Você foi derrotado pelo {inimigo}...")


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
