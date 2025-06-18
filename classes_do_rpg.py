from collections import Counter
import random


itens_1 = {
    "Espada quebrada": {"ataque": 5, "durabilidade": 10},
    "Escudo de madeira": {"defesa": 3, "durabilidade": 15},
    "Poção de cura pequena": {"cura": 10,},
    "katana enferrujada": {"ataque": 7, "durabilidade": 8},  
}  

itens_2 = {
    "Espada longa": {"ataque": 10, "durabilidade": 20},
    "Escudo de ferro": {"defesa": 4, "durabilidade": 20},
    "Poção de cura média": {"cura": 20,},
    "katana afiada": {"ataque": 12, "durabilidade": 15},
}

itens_3 = {
    "Espada Sagrada": {"ataque": 15, "durabilidade": 30},
    "Escudo Forjado": {"defesa": 8, "durabilidade": 35},
    "Poção de cura grande": {"cura": 30,},
    "katana lendária": {"ataque": 20, "durabilidade": 25},
    "cajado do mago supremo": {"ataque": 15, "durabilidade": 28},
}


class Personagem:
    def __init__(self, nome, defesa, forca, inteligencia, classe, habilidade):
        self.nome = nome
        self.vida_maxima = defesa * 10
        self.vida = self.vida_maxima
        self.arcano = inteligencia
        self.forca = forca
        self.defesa = defesa
        self.classe = classe
        self.habilidade = habilidade
        self.inventario = [
            [],  # Armas
            [],  # Armaduras
            []   # Itens/Poções
        ]
        self.xp = 0
        self.nivel = 1
        self.pontos = 0
        self.envenenado = False
        self.turnos_envenenado = 0
        self.furioso = False
        self.ouro = 0
        self.contador_de_baus = 0
        self.arma_equipada = None
        self.armadura_equipada = None
        self.quests_ativas = []
        self.quests_concluidas = []
        self.npc_visitado = {1: False, 2: False, 3: False}

    def recompensa_moedas(self, quantidade):
        self.ouro += quantidade
        print(f"Você recebeu {quantidade} moedas de ouro! Agora tem {self.ouro}.")

    def forca_total(self):
        bonus = self.arma_equipada["ataque"] if self.arma_equipada and "ataque" in self.arma_equipada else 0
        return self.forca + bonus

    def defesa_total(self):
        bonus = self.armadura_equipada["defesa"] if self.armadura_equipada and "defesa" in self.armadura_equipada else 0
        return self.defesa + bonus

    def mostrar_inventario(self):
        categorias = ["Armas", "Armaduras", "Itens"]
        print("\nInventário:")
        arma_nome = self.arma_equipada["nome"] if self.arma_equipada and "nome" in self.arma_equipada else 'Nenhuma'
        armadura_nome = self.armadura_equipada["nome"] if self.armadura_equipada and "nome" in self.armadura_equipada else 'Nenhuma'
        print(f"Itens equipados: Arma: {arma_nome}, Armadura: {armadura_nome}")
        print(f"Vida: {self.vida}/{self.vida_maxima}, XP: {self.xp}, Nível: {self.nivel}, Ouro: {self.ouro}")
        print(f"Atributos - Força: {self.forca_total()}, Defesa: {self.defesa_total()},")
        for i, categoria in enumerate(categorias):
            print(f"\n{categoria}:")
            if not self.inventario[i]:
                print("  (vazio)")
            else:
                for idx, item in enumerate(self.inventario[i], 1):
                    nome = item.get("nome", "Item desconhecido")
                    print(f"  [{idx}] {nome}")

        escolha = input("\nDeseja usar ou equipar algum item? (1-Sim, 2-Não): ")
        if escolha == "1":
            print("Categorias: 1-Armas, 2-Armaduras, 3-Itens")
            try:
                cat = int(input("Escolha a categoria: "))
                if cat < 1 or cat > 3 or not self.inventario[cat-1]:
                    print("Categoria inválida ou vazia.")
                    return
                for idx, item in enumerate(self.inventario[cat-1]):
                    print(f"{idx+1}. {item['nome']}")
                idx_item = int(input("Escolha o número do item: ")) - 1
                if idx_item < 0 or idx_item >= len(self.inventario[cat-1]):
                    print("Item inválido.")
                    return
                item = self.inventario[cat-1][idx_item]
                if cat == 1:
                    self.arma_equipada = item
                    print(f"{self.nome} equipou a arma: {item['nome']}")
                elif cat == 2:
                    self.armadura_equipada = item
                    print(f"{self.nome} equipou a armadura: {item['nome']}")
                elif cat == 3:
                    if "cura" in item:
                        self.curar(item["cura"])
                        self.inventario[2].pop(idx_item)
                        print(f"{item['nome']} acabou!")
                    else:
                        print("Esse item não pode ser usado.")
            except Exception:
                print("Entrada inválida.")
        else:
            print("Ok, voltando ao jogo.")

    def usar_item(self, categoria, item_nome):
        if categoria < 1 or categoria > 3:
            print("Categoria inválida. Escolha entre 1 (Armas), 2 (Armaduras) ou 3 (Itens).")
            return
        for item in self.inventario[categoria - 1]:
            if item.get("nome") == item_nome:
                if categoria == 1:
                    self.arma_equipada = item
                    print(f"{self.nome} equipou a arma {item_nome}.")
                elif categoria == 2:
                    self.armadura_equipada = item
                    print(f"{self.nome} equipou a armadura {item_nome}.")
                elif categoria == 3 and "cura" in item:
                    self.curar(item["cura"])
                    self.inventario[categoria - 1].remove(item)
                    print(f"{self.nome} usou o item {item_nome}.")
                return
        print(f"{item_nome} não encontrado no inventário.")

    def esta_vivo(self):
        return self.vida > 0


    def habilidade_ativa(self, inimigo):
        chance = random.random()
        if chance < 0.3:
            if self.habilidade == "cura":
                cura = random.randint(10, 30)
                self.curar(cura)
            elif self.habilidade == "fúria":
                self.furioso = True
                print(f"{self.nome} entrou em fúria! Ataque dobrado!")
            elif self.habilidade == "veneno":
                inimigo.envenenado = True
                inimigo.turnos_envenenado = 3
                print(f"{self.nome} envenenou {inimigo.nome}!")
            elif self.habilidade == "golpe crítico":
                # Golpe crítico: próximo ataque causa dano dobrado
                self.furioso = True
                print(f"{self.nome} prepara um golpe crítico! Próximo ataque dobrado!")

    def veneno(self):
        if self.envenenado:
            dano = random.randint(5, 15)
            self.vida -= dano
            self.turnos_envenenado -= 1
            print(f"{self.nome} está envenenado! Perdeu {dano} de vida!")
            if self.turnos_envenenado <= 0:
                self.envenenado = False
                print(f"{self.nome} não está mais envenenado!")

    def atacar(self, inimigo):
        self.habilidade_ativa(inimigo)
        ataque_total = random.randint(1, 5) + self.forca_total()
        if self.arma_equipada and "ataque" in self.arma_equipada:
            self.arma_equipada["durabilidade"] -= 1
            if self.arma_equipada["durabilidade"] <= 0:
                print(f"Sua arma {self.arma_equipada['nome']} quebrou!")
                self.arma_equipada = None
        if self.furioso:
            ataque_total *= 2
            print(f"\n{self.nome} está furioso! Ataque dobrado!")
            self.furioso = False
        defesa_total = inimigo.defesa
        if hasattr(inimigo, "armadura_equipada") and inimigo.armadura_equipada and "defesa" in inimigo.armadura_equipada:
            defesa_total += inimigo.armadura_equipada["defesa"]
        dano = max(1, ataque_total - defesa_total + random.randint(-2, 2))
        inimigo.vida -= dano
        print(f"\n{self.nome} atacou {inimigo.nome} e causou {dano} de dano!\n")
        if inimigo.vida <= 0:
            print(f"{inimigo.nome} foi derrotado!")
        else:
            print(f"{inimigo.nome} ainda tem {inimigo.vida} de vida!")

    def curar(self, quantidade):
        cura_total = quantidade + self.arcano  # Inteligência aumenta a cura
        self.vida += cura_total
        if self.vida > self.vida_maxima:
            self.vida = self.vida_maxima
        print(f"{self.nome} se curou e agora tem {self.vida}/{self.vida_maxima} de vida!")

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        print(f"{self.nome} ganhou {quantidade} XP.")
        while self.xp >= self.nivel * 10:
            self.xp -= self.nivel * 10 
            self.nivel += 1
            self.pontos += 3
            print(f"{self.nome} subiu para o nível {self.nivel}!")

    def upar_atributos(self):
        while True:
            if self.pontos > 0:
                print(f"\nPontos disponíveis: {self.pontos}")
                print("1. Aumentar Força")
                print("2. Aumentar Defesa")
                escolha = input("Escolha um atributo para upar: ")
                if escolha == "1":
                    self.forca += 1
                    self.pontos -= 1
                    print(f"Força aumentada para {self.forca}")
                    if self.pontos > 0:
                        continuar = input("Deseja continuar upar atributos? (s/n): ").strip().lower()
                        if continuar not in ['s', 'sim']:
                            print("Saindo do menu de atributos.")
                            break
                elif escolha == "2":
                    self.defesa += 1
                    self.vida_maxima += 10
                    self.vida += 10
                    self.pontos -= 1
                    print(f"Defesa aumentada para {self.defesa}")
                    if self.pontos > 0:
                        continuar = input("Deseja continuar upar atributos? (s/n): ").strip().lower()
                        if continuar not in ['s', 'sim']:
                            print("Saindo do menu de atributos.")
                            break
                else:
                    print("Escolha inválida.")
            else:
                print("Nenhum ponto disponível para upar atributos.")
                break
    def tem_quest(self, quest_id):
        return any(q.id == quest_id for q in self.quests_ativas)

    def ativar_quest(self, quest):
        if not self.tem_quest(quest.id):
            self.quests_ativas.append(quest)

    def checar_quests(self):
        for quest in self.quests_ativas:
            if not quest.concluida and quest.condicao_conclusao(self):
                quest.concluida = True
                if quest not in self.quests_concluidas:
                    self.quests_concluidas.append(quest)
                if callable(quest.recompensa):
                    quest.recompensa(self)
                print(f"Quest '{quest.titulo}' concluída!")

    def __str__(self):
        return f"{self.nome} (Classe: {self.classe})"
    
class NPC:
    def __init__(self, nome, dialogo, quest=None):
        self.nome = nome
        self.dialogo = dialogo
        self.quest = quest

    def falar(self):
        if isinstance(self.dialogo, list):
            for linha in self.dialogo:
                print(linha)
        else:
            print(self.dialogo)

    def oferecer_quest(self, jogador):
        if not self.quest:
            return
        print(f"\n{self.nome} diz:")
        self.falar()
        if not jogador.tem_quest(self.quest.id) and not self.quest.concluida:
            aceita = input("Aceitar missão? (s/n): ").strip().lower()
            if aceita in ['s', 'sim']:
                jogador.ativar_quest(self.quest)
                print(f"Missão '{self.quest.titulo}' ativada!")
            else:
                print("Talvez depois…")
        elif jogador.tem_quest(self.quest.id) and not self.quest.concluida:
            print("Você já ativou essa missão.")
        elif self.quest.concluida:
            print("Você já concluiu essa missão.")

# === CLASSE DO INIMIGO ===
class Inimigo:
    def __init__(self, nome, forca, vida, defesa, nivel, habilidade):
        self.nome = nome
        self.forca = forca
        self.vida_maxima = vida
        self.vida = vida
        self.defesa = defesa
        self.nivel = nivel
        self.habilidade = habilidade
        self.envenenado = False
        self.turnos_envenenado = 0
        self.furioso = False

    def habilidade_ativa(self, jogador):
        chance = random.random()
        if chance < 0.3:
            if self.habilidade == "cura":
                cura = random.randint(10, 20)
                self.curar(cura)
            elif self.habilidade == "fúria":
                self.furioso = True
                print(f"{self.nome} entrou em fúria! Ataque dobrado!")
            elif self.habilidade == "veneno":
                jogador.envenenado = True
                jogador.turnos_envenenado = 3
                print(f"{self.nome} envenenou {jogador.nome}!")

    def atacar(self, jogador):
        self.habilidade_ativa(jogador)
        ataque_total = random.randint(1, self.forca)  # Corrigido de self.ataque para self.forca
        if self.furioso:
            ataque_total *= 2
            print(f"{self.nome} está furioso! Ataque dobrado!")
            self.furioso = False
        dano = max(0, ataque_total - jogador.defesa + random.randint(0, 2))
        jogador.vida -= dano
        print(f"{self.nome} atacou {jogador.nome} e causou {dano} de dano!")
        if jogador.vida <= 0:
            print(f"{jogador.nome} foi derrotado!")
        else:
            print(f"{jogador.nome} ainda tem {jogador.vida} de vida!")

    def veneno(self):
        if self.envenenado:
            dano = random.randint(5, 15)
            self.vida -= dano
            self.turnos_envenenado -= 1
            print(f"{self.nome} está envenenado! Perdeu {dano} de vida!")
            if self.turnos_envenenado <= 0:
                self.envenenado = False
                print(f"{self.nome} não está mais envenenado!")

    def esta_vivo(self):
        return self.vida > 0

    def curar(self, quantidade):
        self.vida += quantidade
        if self.vida > self.vida_maxima:
            self.vida = self.vida_maxima
        print(f"{self.nome} se curou e agora tem {self.vida}/{self.vida_maxima} de vida!")

# === CLASSE DE QUEST ===
class Quest:
    def __init__(self, id, titulo, descricao, condicao_conclusao, recompensa):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.condicao_conclusao = condicao_conclusao
        self.recompensa = recompensa
        self.concluida = False

    def checar(self, jogador):
        if not self.concluida and self.condicao_conclusao(jogador):
            self.concluida = True
            self.recompensa(jogador)
            print(f"Missão '{self.titulo}' concluída!")

# === ESCOLHA DE CLASSE ===
def escolher_classe():
    nome = input("Digite o nome do seu personagem: ")

    print("\nEscolha sua classe:")
    print("1. Guerreiro (vida alta, ataque médio, defesa alta, habilidade: Fúria)")
    print("2. Paladino (vida média, ataque médio, defesa alta, habilidade: Cura)")
    print("3. Samurai (vida média, ataque alto, defesa média, habilidade: Golpe Crítico)")

    opcoes = {
        "1": "Guerreiro",
        "2": "Paladino",
        "3": "Samurai",
        "4": "classe dev"
    }

    while True:
        escolha = input("\nEscolha sua classe e siga em sua jornada: ").lower()
        classe = opcoes.get(escolha)
        if classe:
            break
        else:
            print("Classe inválida, informe novamente por favor.")

    if classe == "Guerreiro":
        jogador = Personagem(nome, defesa=5, forca=5, inteligencia=2, classe=classe, habilidade="fúria")
    elif classe == "Paladino":
        jogador = Personagem(nome, defesa=5, forca=4, inteligencia=4, classe=classe, habilidade="cura")
    elif classe == "Samurai":
        jogador = Personagem(nome, defesa=4, forca=6, inteligencia=2, classe=classe, habilidade="golpe crítico")
    elif classe == "classe dev":
        jogador = Personagem(nome, defesa=100, forca=100, inteligencia=100, classe=classe, habilidade="cura")
        print("Você é um dev! Você tem todos os atributos maximizados!")

    print(f"\nJogador criado com sucesso: {jogador.nome}, da classe {classe}!\n")
    return jogador

# === NARRATIVA E FASES ===
def narrativa_inicio():
    print("\nO mundo está em colapso. O tempo se quebrou em fragmentos.")
    print("Você acorda em uma clareira estranha, com memórias confusas.")
    print("Uma voz misteriosa sussurra: 'Restaure o tempo... ou tudo perecerá.'")
    input("Pressione Enter para continuar...\n")

def exemplo_adicionar_item():
    jogador = Personagem("Nome", defesa=5, forca=5, inteligencia=5, classe="Guerreiro", habilidade="fúria")
    item_nome = "Espada quebrada"
    if item_nome in itens_1:
        item = {"nome": item_nome, **itens_1[item_nome]}
        jogador.inventario[0].append(item)
        print(f"Item '{item_nome}' adicionado ao inventário de {jogador.nome}.")
    else:
        print(f"Item '{item_nome}' não existe em itens_1.")
    return jogador

# Crie o jogador primeiro
jogador = Personagem("Nome", defesa=5, forca=5, inteligencia=5, classe="Guerreiro", habilidade="fúria")

# Agora você pode adicionar itens ao inventário dele
item_nome = "Espada quebrada"
if item_nome in itens_1:
    item = {"nome": item_nome, **itens_1[item_nome]}
    jogador.inventario[0].append(item)
    print(f"Item '{item_nome}' adicionado ao inventário de {jogador.nome}.")
else:
    print(f"Item '{item_nome}' não existe em itens_1.")
