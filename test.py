import pygame
import random
import time

# --- INITIALIZATION ---
pygame.init()

# --- SCREEN DIMENSIONS ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("O Tempo Corre Perigo")

# --- COLORS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# --- FONTS ---
FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)

# --- GAME STATES (Simplified for Pygame) ---
GAME_STATE_TITLE = 0
GAME_STATE_CHARACTER_CREATION = 1
GAME_STATE_EXPLORATION = 2
GAME_STATE_BATTLE = 3
GAME_STATE_VENDOR = 4
GAME_STATE_NPC_INTERACTION = 5
GAME_STATE_GAME_OVER = 6
GAME_STATE_LEVEL_UP = 7
GAME_STATE_QUEST_LOG = 8
GAME_STATE_INVENTORY = 9
GAME_STATE_PORTAL = 10

current_game_state = GAME_STATE_TITLE

# --- Placeholder for game variables (from your original code) ---
local_atual = 1 # This will still track the map/level
inventario = [] # Player's inventory
# ... (Other global variables like itens_1, itens_2, itens_3, inimigos_aleatorios will be needed)

# --- GAME OBJECTS (from your original classes, adapted for Pygame) ---

# --- CLASSE DO JOGADOR (Adapted for Pygame) ---
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
        # Add visual properties
        self.image = pygame.Surface((50, 50)) # Placeholder
        self.image.fill(BLUE) # Player color
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

    def habilidade_ativa(self, target):
        # ... (Your existing logic)
        pass

    def veneno(self):
        # ... (Your existing logic)
        pass

    def atacar(self, inimigo):
        # ... (Your existing logic, will need to update text display)
        pass

    def esta_vivo(self):
        return self.vida > 0

    def curar(self, quantidade):
        # ... (Your existing logic, will need to update text display)
        pass

    def ganhar_xp(self, quantidade):
        # ... (Your existing logic)
        pass

    def upar_atributos(self):
        # This will need to be a Pygame screen/state
        pass

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

# --- CLASSE DOS NPCs (Adapted for Pygame) ---
class NPC:
    def __init__(self, nome, dialogo, quest=None):
        self.nome = nome
        self.dialogo = dialogo
        self.quest = quest
        self.image = pygame.Surface((40, 40)) # Placeholder
        self.image.fill(GREEN) # NPC color
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2))

    def falar(self, screen):
        # This will draw text on the screen instead of printing
        pass

    def oferecer_quest(self, jogador, screen):
        # This will draw text and offer choices on the screen
        pass

# --- CLASSE DO INIMIGO (Adapted for Pygame) ---
class Inimigo:
    def __init__(self, nome, vida, ataque, defesa, habilidade):
        self.nome = nome
        self.vida = vida
        self.vida_maxima = vida
        self.ataque = ataque
        self.defesa = defesa
        self.habilidade = habilidade
        self.envenenado = False
        self.turnos_envenenado = 0
        self.furioso = False
        self.image = pygame.Surface((60, 60)) # Placeholder
        self.image.fill(RED) # Enemy color
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2))

    def habilidade_ativa(self, jogador):
        # ... (Your existing logic)
        pass

    def atacar(self, jogador):
        # ... (Your existing logic, will need to update text display)
        pass

    def veneno(self):
        # ... (Your existing logic)
        pass

    def esta_vivo(self):
        return self.vida > 0

    def curar(self, quantidade):
        # ... (Your existing logic)
        pass

# --- CLASSE DE QUEST ---
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
            # Need to update UI for quest completion

# --- GAME FUNCTIONS (Will be integrated into the Pygame loop) ---

# Initializing global game state variables
player = None
current_enemy = None
current_npc = None
current_dialogue_line = 0

# Functions to draw text on screen
def draw_text(surface, text, color, x, y, font, center_x=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center_x:
        text_rect.centerx = x
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# --- SCREEN RENDERING FUNCTIONS FOR EACH GAME STATE ---

def draw_title_screen():
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "O Tempo Corre Perigo", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, FONT, center_x=True)
    draw_text(SCREEN, "Pressione ENTER para começar", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SMALL_FONT, center_x=True)
    pygame.display.flip()

def draw_character_creation_screen(input_box_text, current_class_options):
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "Criação de Personagem", WHITE, SCREEN_WIDTH // 2, 50, FONT, center_x=True)
    draw_text(SCREEN, "Nome: " + input_box_text, WHITE, SCREEN_WIDTH // 2 - 150, 150, SMALL_FONT)
    draw_text(SCREEN, "Escolha sua classe:", WHITE, SCREEN_WIDTH // 2 - 150, 200, SMALL_FONT)
    for i, (key, value) in enumerate(current_class_options.items()):
        draw_text(SCREEN, f"{key}. {value}", WHITE, SCREEN_WIDTH // 2 - 150, 230 + i * 30, SMALL_FONT)
    pygame.display.flip()

def draw_exploration_screen():
    SCREEN.fill(BLUE) # Representing a map background
    draw_text(SCREEN, f"Local Atual: {get_map_name(local_atual)}", WHITE, 50, 50, FONT)
    draw_text(SCREEN, f"Vida: {player.vida}/{player.vida_maxima}", WHITE, 50, 100, SMALL_FONT)
    draw_text(SCREEN, f"Ouro: {player.ouro}", YELLOW, 50, 130, SMALL_FONT)
    draw_text(SCREEN, "O que você quer fazer?", WHITE, 50, 200, FONT)
    draw_text(SCREEN, "1. Explorar", WHITE, 50, 250, SMALL_FONT)
    draw_text(SCREEN, "2. Inventário", WHITE, 50, 280, SMALL_FONT)
    draw_text(SCREEN, "3. Quests", WHITE, 50, 310, SMALL_FONT)
    draw_text(SCREEN, "4. Interagir (se houver NPC/Vendedor)", WHITE, 50, 340, SMALL_FONT)
    # Draw player character
    SCREEN.blit(player.image, player.rect)
    pygame.display.flip()

def draw_battle_screen(current_enemy, battle_log):
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "Batalha!", WHITE, SCREEN_WIDTH // 2, 50, FONT, center_x=True)

    # Player stats
    draw_text(SCREEN, f"{player.nome}: {player.vida}/{player.vida_maxima} HP", GREEN, 50, 100, SMALL_FONT)
    # Enemy stats
    draw_text(SCREEN, f"{current_enemy.nome}: {current_enemy.vida}/{current_enemy.vida_maxima} HP", RED, SCREEN_WIDTH - 200, 100, SMALL_FONT)

    # Actions
    draw_text(SCREEN, "Escolha sua ação:", WHITE, 50, SCREEN_HEIGHT - 150, SMALL_FONT)
    draw_text(SCREEN, "1. Atacar", WHITE, 50, SCREEN_HEIGHT - 120, SMALL_FONT)
    draw_text(SCREEN, "2. Esquivar", WHITE, 50, SCREEN_HEIGHT - 90, SMALL_FONT)
    draw_text(SCREEN, "3. Usar Poção", WHITE, 50, SCREEN_HEIGHT - 60, SMALL_FONT)

    # Battle log
    y_offset = 200
    for log_entry in battle_log[-5:]: # Show last 5 messages
        draw_text(SCREEN, log_entry, WHITE, 50, y_offset, SMALL_FONT)
        y_offset += 25

    # Draw player and enemy (simple rectangles for now)
    SCREEN.blit(player.image, player.rect)
    SCREEN.blit(current_enemy.image, current_enemy.rect)

    pygame.display.flip()

def draw_vendor_screen(vendor_items, current_dialogue_line):
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "Vendedor", WHITE, SCREEN_WIDTH // 2, 50, FONT, center_x=True)
    draw_text(SCREEN, f"Você tem {player.ouro} moedas.", YELLOW, SCREEN_WIDTH // 2, 100, SMALL_FONT, center_x=True)
    draw_text(SCREEN, "Itens à venda:", WHITE, 50, 150, SMALL_FONT)

    y_offset = 180
    for i, (item_name, price) in enumerate(vendor_items.items()):
        draw_text(SCREEN, f"{i+1}. {item_name} - {price} Moedas", WHITE, 50, y_offset, SMALL_FONT)
        y_offset += 30
    draw_text(SCREEN, "Pressione 'Q' para sair.", WHITE, 50, y_offset + 30, SMALL_FONT)
    pygame.display.flip()

def draw_npc_interaction_screen(npc_dialogue, current_dialogue_line, player_has_quest):
    SCREEN.fill(BLACK)
    draw_text(SCREEN, current_npc.nome, WHITE, SCREEN_WIDTH // 2, 50, FONT, center_x=True)
    
    if current_dialogue_line < len(npc_dialogue):
        draw_text(SCREEN, npc_dialogue[current_dialogue_line], WHITE, 50, 150, SMALL_FONT)
        draw_text(SCREEN, "Pressione ENTER para continuar...", WHITE, 50, SCREEN_HEIGHT - 50, SMALL_FONT)
    else:
        if not player_has_quest and current_npc.quest and not current_npc.quest.concluida:
            draw_text(SCREEN, "Aceitar missão? (S/N)", WHITE, 50, 150, SMALL_FONT)
        elif player_has_quest and current_npc.quest and not current_npc.quest.concluida:
             draw_text(SCREEN, "Você já ativou essa missão.", WHITE, 50, 150, SMALL_FONT)
        elif current_npc.quest and current_npc.quest.concluida:
            draw_text(SCREEN, "Você já concluiu essa missão.", WHITE, 50, 150, SMALL_FONT)
        else:
            draw_text(SCREEN, "Pressione 'Q' para sair.", WHITE, 50, SCREEN_HEIGHT - 50, SMALL_FONT)
    
    pygame.display.flip()

def draw_game_over_screen():
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "GAME OVER", RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, FONT, center_x=True)
    draw_text(SCREEN, "Pressione 'R' para Reiniciar ou 'Q' para Sair", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SMALL_FONT, center_x=True)
    pygame.display.flip()

def draw_level_up_screen():
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "Você subiu de nível!", GREEN, SCREEN_WIDTH // 2, 50, FONT, center_x=True)
    draw_text(SCREEN, f"Pontos disponíveis: {player.pontos}", WHITE, 50, 150, SMALL_FONT)
    draw_text(SCREEN, "Escolha um atributo para upar:", WHITE, 50, 200, SMALL_FONT)
    draw_text(SCREEN, "1. Aumentar Força", WHITE, 50, 230, SMALL_FONT)
    draw_text(SCREEN, "2. Aumentar Defesa", WHITE, 50, 260, SMALL_FONT)
    draw_text(SCREEN, "3. Aumentar Inteligência", WHITE, 50, 290, SMALL_FONT)
    pygame.display.flip()

def draw_inventory_screen():
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "Inventário", WHITE, SCREEN_WIDTH // 2, 50, FONT, center_x=True)
    if player.inventario:
        y_offset = 100
        for i, item in enumerate(player.inventario):
            draw_text(SCREEN, f"- {item}", WHITE, 50, y_offset + i * 30, SMALL_FONT)
    else:
        draw_text(SCREEN, "Seu inventário está vazio.", WHITE, 50, 100, SMALL_FONT)
    draw_text(SCREEN, "Pressione 'Q' para sair.", WHITE, 50, SCREEN_HEIGHT - 50, SMALL_FONT)
    pygame.display.flip()

def draw_quest_log_screen():
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "Missões Ativas", WHITE, SCREEN_WIDTH // 2, 50, FONT, center_x=True)
    if player.quests_ativas:
        y_offset = 100
        for i, quest in enumerate(player.quests_ativas):
            status = "Concluída" if quest.concluida else "Ativa"
            draw_text(SCREEN, f"{i+1}. {quest.titulo} ({status})", WHITE, 50, y_offset + i * 30, SMALL_FONT)
            draw_text(SCREEN, f"   - {quest.descricao}", WHITE, 70, y_offset + i * 30 + 25, SMALL_FONT)
            y_offset += 60
    else:
        draw_text(SCREEN, "Nenhuma missão ativa.", WHITE, 50, 100, SMALL_FONT)
    draw_text(SCREEN, "Pressione 'Q' para sair.", WHITE, 50, SCREEN_HEIGHT - 50, SMALL_FONT)
    pygame.display.flip()

def draw_portal_screen():
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "O PORTAL!", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, FONT, center_x=True)
    draw_text(SCREEN, "Digite o código para abrir o portal:", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SMALL_FONT, center_x=True)
    pygame.display.flip()


# --- GAME LOGIC FUNCTIONS (Adapted for Pygame) ---

def choose_class_pygame(input_box_text):
    global player, current_game_state
    
    # This will be handled by keyboard input in the event loop
    opcoes = {
        "1": "Guerreiro",
        "2": "Mago",
        "3": "Arqueiro",
        "4": "classe dev"
    }
    
    # For now, let's assume 'input_box_text' holds the class choice (e.g., "1")
    # In a real Pygame app, you'd use a more robust input handling for character creation
    class_choice = input_box_text.strip()
    
    if class_choice in opcoes:
        chosen_class_name = opcoes[class_choice]
        if chosen_class_name == "Guerreiro":
            player = Personagem("Hero", defesa=7, forca=6, inteligencia=3, classe=chosen_class_name, habilidade="fúria")
        elif chosen_class_name == "Mago":
            player = Personagem("Hero", defesa=3, forca=4, inteligencia=8, classe=chosen_class_name, habilidade="cura")
        elif chosen_class_name == "Arqueiro":
            player = Personagem("Hero", defesa=5, forca=7, inteligencia=4, classe=chosen_class_name, habilidade="veneno")
        elif chosen_class_name == "classe dev":
            player = Personagem("Hero", defesa=100, forca=100, inteligencia=100, classe=chosen_class_name, habilidade="cura")
        
        print(f"Jogador criado: {player.nome}, Classe: {player.classe}") # Debug print
        current_game_state = GAME_STATE_EXPLORATION # Move to exploration after creation
        return True
    return False

def condicao_coletar_3_baus(jogador):
    return jogador.contador_de_baus >= 3

def recompensa_moedas_50(jogador):
    jogador.ouro += 50
    print("Você ganhou 50 moedas!") # Debug print

def nova_quest_baus():
    return Quest(
        id='baus_1',
        titulo='Caçador de Baús',
        descricao='Encontre 3 baús misteriosos na Lagoa dos Dragões.',
        condicao_conclusao=condicao_coletar_3_baus,
        recompensa=recompensa_moedas_50
    )

quest_baus = nova_quest_baus()

npc_fase1 = NPC(
    nome='Samurai Aposentado',
    dialogo=[
        'Ah, jovem aventureiro…',
        'Preciso que você recupere 3 baús perdidos.',
        'Eles estão espalhados pela Lagoa dos Dragões.'
    ],
    quest=quest_baus
)

npc_fase2 = NPC(
    nome='Dio Cavalheiro Esquecido',
    dialogo=[
        'Ah, jovem aventureiro…',
        'Preciso que você recupere 3 baús perdidos.',
        'Eles estão espalhados pelo Berço de Kharzuth.'
    ],
    quest=nova_quest_baus() # Each NPC should offer a fresh quest if needed, or share
)

npc_fase3 = NPC(
    nome='Neo Necromante do Tempo',
    dialogo=[
        'Ah, jovem aventureiro…',
        'Preciso que você recupere 3 baús perdidos.',
        'Eles estão espalhados pelo Castelo de Drenvaar.'
    ],
    quest=nova_quest_baus()
)

def get_map_name(map_id):
    if map_id == 1: return "Lagoa dos Dragões"
    if map_id == 2: return "Berço de Kharzuth"
    if map_id == 3: return "Castelo de Drenvaar"
    return "Local Desconhecido"

# Global variable for battle log
battle_log = []

def perform_battle_action(action_choice):
    global current_game_state, battle_log, player, current_enemy
    
    battle_log = [] # Clear log for new turn

    if action_choice == '1': # Atacar
        player.atacar(current_enemy)
        battle_log.append(f"{player.nome} atacou {current_enemy.nome} e causou {max(0, player.forca - current_enemy.defesa)} de dano!")
    elif action_choice == '2': # Esquivar
        esquiva_chance = random.random()
        if esquiva_chance < 0.5:
            battle_log.append("Esquiva efetuada com sucesso!")
        else:
            battle_log.append("Esquiva falhou!")
            # Enemy still attacks
    elif action_choice == '3': # Usar poção
        player.curar(30)
        battle_log.append(f"{player.nome} usou uma poção e curou 30 HP.")
    
    # Enemy turn if still alive
    if current_enemy.esta_vivo():
        current_enemy.atacar(player)
        battle_log.append(f"{current_enemy.nome} atacou {player.nome}!")
        player.veneno() # Check for player poison
        current_enemy.veneno() # Check for enemy poison

    # Check for battle end conditions
    if not player.esta_vivo():
        battle_log.append(f"{player.nome} foi derrotado!")
        current_game_state = GAME_STATE_GAME_OVER
    elif not current_enemy.esta_vivo():
        battle_log.append(f"{current_enemy.nome} foi derrotado!")
        player.ganhar_xp(10)
        current_game_state = GAME_STATE_EXPLORATION # Return to exploration
        if player.pontos > 0:
            current_game_state = GAME_STATE_LEVEL_UP # Go to level up if points available

def handle_exploration_event():
    global current_game_state, current_enemy, current_npc, local_atual

    events = ["inimigo", "bau", "npc", "nada", "vendedor"]
    event_weights = [0.3, 0.3, 0.2, 0.1, 0.1]
    
    # Adjust event weights based on map and quest progress (more intelligent)
    if player.contador_de_baus < 3 and current_game_state == GAME_STATE_EXPLORATION:
        event_weights[1] += 0.2 # Increase chance of finding a chest if quest active
        event_weights[0] -= 0.1 # Decrease enemy chance slightly
    
    chosen_event = random.choices(events, weights=event_weights)[0]

    if chosen_event == "inimigo":
        enemy_name = random.choice(inimigos_aleatorios)
        # Scale enemy stats based on player level or map level
        enemy_vida = 10 + player.nivel * 2
        enemy_ataque = 3 + player.nivel
        enemy_defesa = 1 + player.nivel // 2
        enemy_hability = random.choice(["furia", "veneno", "cura", None])
        current_enemy = Inimigo(enemy_name, enemy_vida, enemy_ataque, enemy_defesa, enemy_hability)
        print(f"Você encontrou um {enemy_name}!")
        global battle_log
        battle_log = [] # Clear previous battle log
        current_game_state = GAME_STATE_BATTLE

    elif chosen_event == "bau":
        item_found = random.choice(list(itens_1.keys())) # Or itens_2, itens_3 based on local_atual
        player.inventario.append(item_found)
        player.contador_de_baus += 1
        print(f"Você encontrou um baú e coletou: {item_found}! Baús encontrados: {player.contador_de_baus}/3")
        player.checar_quests() # Check quests after finding a chest

    elif chosen_event == "npc":
        if local_atual == 1: current_npc = npc_fase1
        elif local_atual == 2: current_npc = npc_fase2
        elif local_atual == 3: current_npc = npc_fase3
        print(f"Você encontrou {current_npc.nome}.")
        global current_dialogue_line
        current_dialogue_line = 0 # Reset dialogue
        current_game_state = GAME_STATE_NPC_INTERACTION

    elif chosen_event == "vendedor":
        print("Você encontrou um vendedor!")
        current_game_state = GAME_STATE_VENDOR
    
    elif chosen_event == "nada":
        print("Você explorou e não encontrou nada interessante...")

# Dummy item lists for demonstration
itens_1 = {
    "Espada quebrada": {"ataque": 5, "durabilidade": 10},
    "Escudo de madeira": {"defesa": 3, "durabilidade": 15},
    "Poção de cura pequena": {"cura": 10, "quantidade": 1},
    "katana enferrujada": {"ataque": 7, "durabilidade": 8},    
}

itens_2 = {
    "Espada longa": {"ataque": 10, "durabilidade": 20},
    "Escudo de ferro": {"defesa": 5, "durabilidade": 25},
    "Poção de cura média": {"cura": 20, "quantidade": 1},
    "katana afiada": {"ataque": 12, "durabilidade": 15},
}

itens_3 = {
    "Espada Sagrada": {"ataque": 15, "durabilidade": 30},
    "Escudo Forjado": {"defesa": 8, "durabilidade": 35},
    "Poção de cura grande": {"cura": 30, "quantidade": 1},
    "katana lendária": {"ataque": 20, "durabilidade": 25},
    "cajado do mago supremo": {"ataque": 15, "durabilidade": 28},
}

inimigos_aleatorios = [
    "Goblin", "Esqueleto", "Orc", "Slime", "Lobo Sangrento", "Espectro", "morto-vivo", "minotauro"
]

vendor_items = {
    "Espada de madeira": 10,
    "Escudo de madeira": 10,
    "Poção de cura pequena": 15
}

# --- MAIN GAME LOOP ---
running = True
player_name_input = ""
class_options_display = {
    "1": "Guerreiro (vida alta, ataque médio, defesa alta)",
    "2": "Mago (vida baixa, ataque alto, defesa baixa)",
    "3": "Arqueiro (vida média, ataque médio-alto, defesa média)",
    "4": "Classe Dev (DEBUG - ATRIBUTOS MAXIMIZADOS)"
}

# For NPC interaction
npc_dialogue_finished = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # --- TITLE SCREEN EVENT HANDLING ---
        if current_game_state == GAME_STATE_TITLE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_game_state = GAME_STATE_CHARACTER_CREATION
        
        # --- CHARACTER CREATION EVENT HANDLING ---
        elif current_game_state == GAME_STATE_CHARACTER_CREATION:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # After typing name, allow choosing class.
                    # For simplicity, let's assume '1' (Guerreiro) is chosen if Enter is pressed after name.
                    # In a real game, you'd have dedicated class selection buttons/input.
                    if player_name_input: # If name is entered
                        if not player: # If player not created yet, use a default class or prompt for class
                            # For simplicity, let's create a Warrior with the entered name
                            player = Personagem(player_name_input, defesa=7, forca=6, inteligencia=3, classe="Guerreiro", habilidade="fúria")
                            current_game_state = GAME_STATE_EXPLORATION
                            print(f"Player '{player_name_input}' (Guerreiro) created!") # Debug
                        elif player: # If class is being chosen
                            # Assuming the input box can also capture class choice
                            # This needs more robust UI for class selection
                            pass # Handled by direct class choice input
                elif event.key == pygame.K_BACKSPACE:
                    player_name_input = player_name_input[:-1]
                else:
                    player_name_input += event.unicode
                
                # Manual class selection (simple for now)
                if event.key == pygame.K_1:
                    choose_class_pygame("1")
                elif event.key == pygame.K_2:
                    choose_class_pygame("2")
                elif event.key == pygame.K_3:
                    choose_class_pygame("3")
                elif event.key == pygame.K_4:
                    choose_class_pygame("4") # Dev class
        
        # --- EXPLORATION EVENT HANDLING ---
        elif current_game_state == GAME_STATE_EXPLORATION:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: # Explore
                    handle_exploration_event()
                elif event.key == pygame.K_2: # Inventory
                    current_game_state = GAME_STATE_INVENTORY
                elif event.key == pygame.K_3: # Quests
                    current_game_state = GAME_STATE_QUEST_LOG
                elif event.key == pygame.K_4: # Interact (if NPC/Vendor is near)
                    # This needs logic to check if NPC or vendor is actually present
                    # For now, let's just assume if current_npc is set, we go to NPC interaction
                    if current_npc:
                        current_game_state = GAME_STATE_NPC_INTERACTION
                        current_dialogue_line = 0 # Reset dialogue
                    elif random.random() < 0.5: # Simple chance to find a vendor if '4' is pressed and no NPC
                        current_game_state = GAME_STATE_VENDOR
                    else:
                        print("Não há nada para interagir por perto.") # Debug
        
        # --- BATTLE EVENT HANDLING ---
        elif current_game_state == GAME_STATE_BATTLE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: # Attack
                    perform_battle_action('1')
                elif event.key == pygame.K_2: # Dodge
                    perform_battle_action('2')
                elif event.key == pygame.K_3: # Use Potion
                    perform_battle_action('3')
        
        # --- VENDOR EVENT HANDLING ---
        elif current_game_state == GAME_STATE_VENDOR:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # Quit vendor screen
                    current_game_state = GAME_STATE_EXPLORATION
                elif event.key == pygame.K_1: # Buy Espada de madeira
                    if player.ouro >= 10:
                        player.ouro -= 10
                        player.inventario.append("Espada de madeira")
                        print("Você comprou uma Espada de madeira!")
                    else:
                        print("Moedas insuficientes!")
                elif event.key == pygame.K_2: # Buy Escudo de madeira
                    if player.ouro >= 10:
                        player.ouro -= 10
                        player.inventario.append("Escudo de madeira")
                        print("Você comprou um Escudo de madeira!")
                    else:
                        print("Moedas insuficientes!")
                elif event.key == pygame.K_3: # Buy Poção de cura pequena
                    if player.ouro >= 15:
                        player.ouro -= 15
                        player.inventario.append("Poção de cura pequena")
                        print("Você comprou uma Poção de cura pequena!")
                    else:
                        print("Moedas insuficientes!")

        # --- NPC INTERACTION EVENT HANDLING ---
        elif current_game_state == GAME_STATE_NPC_INTERACTION:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_dialogue_line < len(current_npc.dialogo):
                        current_dialogue_line += 1
                    else: # Dialogue finished
                        if current_npc.quest and not player.tem_quest(current_npc.quest.id) and not current_npc.quest.concluida:
                            # Prompt to accept quest (handled by 'S' or 'N' press)
                            pass 
                        else:
                            current_game_state = GAME_STATE_EXPLORATION # Exit interaction if dialogue and quest handled
                elif event.key == pygame.K_s and current_dialogue_line >= len(current_npc.dialogo): # Accept quest
                    if current_npc.quest and not player.tem_quest(current_npc.quest.id) and not current_npc.quest.concluida:
                        player.ativar_quest(current_npc.quest)
                        print(f"Missão '{current_npc.quest.titulo}' ativada!")
                        current_game_state = GAME_STATE_EXPLORATION
                elif event.key == pygame.K_n and current_dialogue_line >= len(current_npc.dialogo): # Decline quest
                    if current_npc.quest and not player.tem_quest(current_npc.quest.id) and not current_npc.quest.concluida:
                        print("Talvez depois…")
                        current_game_state = GAME_STATE_EXPLORATION
                elif event.key == pygame.K_q: # Quit interaction
                    current_game_state = GAME_STATE_EXPLORATION

        # --- GAME OVER EVENT HANDLING ---
        elif current_game_state == GAME_STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Restart
                    # Reset game state and player
                    player = None
                    player_name_input = ""
                    current_game_state = GAME_STATE_TITLE
                    local_atual = 1
                elif event.key == pygame.K_q: # Quit
                    running = False
        
        # --- LEVEL UP EVENT HANDLING ---
        elif current_game_state == GAME_STATE_LEVEL_UP:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and player.pontos > 0:
                    player.forca += 1
                    player.pontos -= 1
                    print(f"Força aumentada para {player.forca}")
                elif event.key == pygame.K_2 and player.pontos > 0:
                    player.defesa += 1
                    player.vida_maxima += 10
                    player.vida += 10
                    player.pontos -= 1
                    print(f"Defesa aumentada para {player.defesa}")
                elif event.key == pygame.K_3 and player.pontos > 0:
                    player.arcano += 1
                    player.pontos -= 1
                    print(f"Inteligência aumentada para {player.arcano}")
                
                if player.pontos == 0: # All points spent
                    current_game_state = GAME_STATE_EXPLORATION
                elif event.key == pygame.K_q: # Option to quit level up screen early
                    current_game_state = GAME_STATE_EXPLORATION
        
        # --- INVENTORY / QUEST LOG EVENT HANDLING ---
        elif current_game_state in [GAME_STATE_INVENTORY, GAME_STATE_QUEST_LOG]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # Quit inventory/quest log
                    current_game_state = GAME_STATE_EXPLORATION

    # --- DRAWING BASED ON CURRENT GAME STATE ---
    if current_game_state == GAME_STATE_TITLE:
        draw_title_screen()
    elif current_game_state == GAME_STATE_CHARACTER_CREATION:
        draw_character_creation_screen(player_name_input, class_options_display)
    elif current_game_state == GAME_STATE_EXPLORATION:
        draw_exploration_screen()
    elif current_game_state == GAME_STATE_BATTLE:
        draw_battle_screen(current_enemy, battle_log)
    elif current_game_state == GAME_STATE_VENDOR:
        draw_vendor_screen(vendor_items, current_dialogue_line) # dialogue_line is not used here, remove it
    elif current_game_state == GAME_STATE_NPC_INTERACTION:
        # Pass the current NPC's dialogue and check if the player has the quest
        if current_npc:
            player_has_quest = player.tem_quest(current_npc.quest.id) if current_npc.quest else False
            draw_npc_interaction_screen(current_npc.dialogo, current_dialogue_line, player_has_quest)
    elif current_game_state == GAME_STATE_GAME_OVER:
        draw_game_over_screen()
    elif current_game_state == GAME_STATE_LEVEL_UP:
        draw_level_up_screen()
    elif current_game_state == GAME_STATE_INVENTORY:
        draw_inventory_screen()
    elif current_game_state == GAME_STATE_QUEST_LOG:
        draw_quest_log_screen()
    elif current_game_state == GAME_STATE_PORTAL:
        draw_portal_screen()

pygame.quit()