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
        self.inventario = []
        self.xp = 0
        self.nivel = 1
        self.pontos = 0
        self.envenenado = False
        self.turnos_envenenado = 0
        self.furioso = False
        self.ouro = 0
        self.contador_de_baus = 0
        self.quests_ativas = []
        self.quests_concluidas = []

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
        ataque_total = random.randint(1,5) + self.forca
        if self.furioso:
            ataque_total *= 2
            print(f"\n{self.nome} está furioso! Ataque dobrado!")
            self.furioso = False
        dano = max(0, ataque_total - inimigo.defesa + random.randint(-2, 2))
        inimigo.vida -= dano
        print(f"\n{self.nome} atacou {inimigo.nome} e causou {dano} de dano!\n")
        if inimigo.vida <= 0:
            print(f"{inimigo.nome} foi derrotado!")
        else:
            print(f"{inimigo.nome} ainda tem {inimigo.vida} de vida!")

    def esta_vivo(self):
        return self.vida > 0

    def curar(self, quantidade):
        self.vida += quantidade
        if self.vida > self.vida_maxima:
            self.vida = self.vida_maxima
        print(f"{self.nome} se curou e agora tem {self.vida}/{self.vida_maxima} de vida!")

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        if self.xp >= self.nivel * 10:
            self.nivel += 1
            self.pontos += 3
            print(f"{self.nome} subiu para o nível {self.nivel}!")
            self.upar_atributos()

    def upar_atributos(self):
        while self.pontos > 0:
            print(f"\nPontos disponíveis: {self.pontos}")
            print("1. Aumentar Força")
            print("2. Aumentar Defesa")
            print("3. Aumentar Inteligência")
            escolha = input("Escolha um atributo para upar: ")
            if escolha == "1":
                self.forca += 1
                self.pontos -= 1
                print(f"Força aumentada para {self.forca}")
            elif escolha == "2":
                self.defesa += 1
                self.vida_maxima += 10
                self.vida += 10
                self.pontos -= 1
                print(f"Defesa aumentada para {self.defesa}")
            elif escolha == "3":
                self.arcano += 1
                self.pontos -= 1
                print(f"Inteligência aumentada para {self.arcano}")
            else:
                print("Escolha inválida.")

    def tem_quest(self, quest_id):
        return any(q.id == quest_id for q in self.quests_ativas)

    def ativar_quest(self, quest):
        if not self.tem_quest(quest.id):
            self.quests_ativas.append(quest)

    def checar_quests(self):
        for quest in self.quests_ativas:
            quest.checar(self)
            if quest.concluida and quest not in self.quests_concluidas:
                self.quests_concluidas.append(quest)

    def _str_(self):
        return f"{self.nome} (Classe: {self.classe})"