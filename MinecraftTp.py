import random
import socket

# === CLASSES PRINCIPALES ===

# Classe Player pour gérer les joueurs
class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100  # Points de vie
        self.attack = 10  # Points d'attaque
        self.defense = 5  # Points de défense
        self.inventory = []  # Inventaire

    def take_damage(self, dmg):
        # Réduction des dégâts en fonction des points de défense
        damage_taken = max(0, dmg - self.defense)
        self.hp -= damage_taken
        return damage_taken

    def attack_player(self, other_player):
        # Attaque un autre joueur
        damage = self.attack
        damage_taken = other_player.take_damage(damage)
        print(f"{self.name} attaque {other_player.name} et inflige {damage_taken} dégâts.")

    def add_to_inventory(self, item):
        # Ajoute un objet à l'inventaire
        self.inventory.append(item)

    def show_inventory(self):
        # Affiche le contenu de l'inventaire
        print(f"Inventaire de {self.name}: {self.inventory}")

# Classe Block pour les ressources
class Block:
    def __init__(self, block_type, is_collectible=True):
        self.block_type = block_type
        self.is_collectible = is_collectible

    def __str__(self):
        return self.block_type

# Classe CraftTable pour gérer le crafting
class CraftTable:
    recipes = {
        "sword": ["wood", "iron"],
        "armor": ["copper", "copper", "copper"]
    }

    @staticmethod
    def craft(item_name, inventory):
        # Vérifie si les matériaux nécessaires sont disponibles
        if item_name in CraftTable.recipes:
            recipe = CraftTable.recipes[item_name]
            if all(material in inventory for material in recipe):
                for material in recipe:
                    inventory.remove(material)  # Retire les matériaux utilisés
                print(f"{item_name} créé avec succès!")
                return item_name
            else:
                print("Matériaux manquants pour créer cet objet.")
        return None

# === MÉCANIQUES DE JEU ===

# Fonction pour le déplacement dans le monde
def move(player):
    event = random.choice(["block", "enemy", "nothing"])
    if event == "block":
        block = Block(random.choice(["wood", "iron", "food"]))
        print(f"Tu as trouvé un {block}!")
        if block.is_collectible:
            player.add_to_inventory(block.block_type)
    elif event == "enemy":
        print("Un ennemi apparaît! Prépare-toi à te battre.")
    else:
        print("Rien ne s'est passé.")

# === MULTIJOUEUR : SERVEUR SIMPLE ===

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 5555))
    server.listen(2)
    print("Serveur prêt, en attente de joueurs...")

    players = []
    while len(players) < 2:
        conn, addr = server.accept()
        print(f"Joueur connecté depuis {addr}")
        players.append(conn)

    # Combat PvP en 5 tours
    for i in range(5):
        for player in players:
            player.send(b"C'est ton tour! Tape 'attaque'.\n")
            response = player.recv(1024)
            print(f"Action du joueur : {response.decode()}")

    server.close()

# === INTERFACE CONSOLE ===

def game_menu():
    print("Bienvenue dans le jeu Minecraft simplifié!")
    player = Player(input("Entre ton nom de joueur : "))

    while True:
        print("\nActions disponibles :")
        print("1. Se déplacer")
        print("2. Afficher l'inventaire")
        print("3. Crafter un objet")
        print("4. Quitter")
        choice = input("Choisis une action : ")

        if choice == "1":
            move(player)
        elif choice == "2":
            player.show_inventory()
        elif choice == "3":
            item = input("Quel objet veux-tu crafter ? ")
            CraftTable.craft(item, player.inventory)
        elif choice == "4":
            print("Merci d'avoir joué!")
            break
        else:
            print("Choix invalide, essaie encore.")

# === LANCEMENT DU JEU ===

if __name__ == "__main__":
    game_menu()
