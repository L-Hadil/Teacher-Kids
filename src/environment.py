import random
import pygame

class Environment:
    def __init__(self, width, height, cell_size, candy_zone, coloring_zone, candy_count, candy_icon_path, potion_icon_path):
        """
        Initialise l'environnement avec des bonbons, une zone de coloriage, et des potions.
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.candy_zone = candy_zone
        self.coloring_zone = coloring_zone
        self.candy_count = candy_count
        self.candy_icon = pygame.image.load(candy_icon_path)
        self.candy_icon = pygame.transform.scale(self.candy_icon, (cell_size, cell_size))

        # Gestion des potions
        self.potion_icon = pygame.image.load(potion_icon_path)
        self.potion_icon = pygame.transform.scale(self.potion_icon, (cell_size, cell_size))
        self.potions = [  # Trois potions avec leur état
            {"position": None, "active": False},
            {"position": None, "active": False},
            {"position": None, "active": False},
        ]
        self.potion_interval = 10000  # Intervalle réduit à 10 secondes
        self.last_potion_time = pygame.time.get_ticks()

    def is_valid_potion_position(self, x, y):
        """
        Vérifie si une position est en dehors des zones interdites (coloriage et bonbons).

        Args:
        - x (int): Position X.
        - y (int): Position Y.

        Returns:
        - bool: True si la position est valide, False sinon.
        """
        in_coloring_zone = (self.coloring_zone[0] <= x <= self.coloring_zone[2] and
                            self.coloring_zone[1] <= y <= self.coloring_zone[3])
        in_candy_zone = (self.candy_zone[0] <= x <= self.candy_zone[2] and
                         self.candy_zone[1] <= y <= self.candy_zone[3])
        return not (in_coloring_zone or in_candy_zone)

    def generate_potion_positions(self):
        """
        Génère des positions valides pour les trois potions.
        """
        for potion in self.potions:
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if self.is_valid_potion_position(x, y):
                    potion["position"] = (x, y)
                    potion["active"] = True
                    break

    def update_potions(self):
        """
        Met à jour les potions pour les faire apparaître si nécessaire.
        """
        current_time = pygame.time.get_ticks()
        for potion in self.potions:
            if not potion["active"]:  # Si une potion est inactive, la réactiver
                if current_time - self.last_potion_time >= self.potion_interval:
                    self.generate_potion_positions()
                    self.last_potion_time = current_time

    def is_potion_at(self, x, y):
        """
        Vérifie si une potion est présente à une position donnée.

        Args:
        - x (int): Position X.
        - y (int): Position Y.

        Returns:
        - dict: Potion correspondante si elle est présente, sinon None.
        """
        for potion in self.potions:
            if potion["active"] and potion["position"] == (x, y):
                return potion
        return None

    def is_candy_at(self, x, y):
        """
        Vérifie si un bonbon est présent à une position donnée.

        Args:
        - x (int): Coordonnée X.
        - y (int): Coordonnée Y.

        Returns:
        - bool: True si un bonbon est présent à cette position, False sinon.
        """
        # Vérifie si la position est dans la zone des bonbons et qu'il reste des bonbons
        return (self.candy_zone[0] <= x <= self.candy_zone[2] and
                self.candy_zone[1] <= y <= self.candy_zone[3] and
                self.candy_count > 0)

    def collect_potion(self, x, y):
        """
        Supprime une potion lorsqu'elle est ramassée.

        Args:
        - x (int): Position X de la potion.
        - y (int): Position Y de la potion.

        Returns:
        - dict: Potion correspondante si elle est ramassée, sinon None.
        """
        for potion in self.potions:
            if potion["position"] == (x, y) and potion["active"]:
                potion["active"] = False
                potion["position"] = None  # Supprime la position
                print(f"Potion at ({x}, {y}) was eaten!")
                return potion
        return None

    def draw(self, screen):
        """
        Dessine la grille, les zones, les bonbons et les potions.
        """
        # Dessiner toutes les cases de la grille (espace neutre)
        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (211, 211, 211), rect)  # Gris clair pour l'espace neutre
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Bordures noires

        # Dessiner la zone de coloriage
        for x in range(self.coloring_zone[0], self.coloring_zone[2] + 1):
            for y in range(self.coloring_zone[1], self.coloring_zone[3] + 1):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (144, 238, 144), rect)  # Vert clair pour la zone de coloriage
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Bordures noires

        # Dessiner la zone des bonbons
        for x in range(self.candy_zone[0], self.candy_zone[2] + 1):
            for y in range(self.candy_zone[1], self.candy_zone[3] + 1):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 239, 213), rect)  # Beige pour la zone des bonbons
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Bordures noires

        # Afficher les bonbons (quantité limitée)
        count = 0
        for x in range(self.candy_zone[0], self.candy_zone[2] + 1):
            for y in range(self.candy_zone[1], self.candy_zone[3] + 1):
                if count < self.candy_count:
                    screen.blit(self.candy_icon, (x * self.cell_size, y * self.cell_size))
                    count += 1

        # Dessiner les potions
        for potion in self.potions:
            if potion["active"]:
                x, y = potion["position"]
                screen.blit(self.potion_icon, (x * self.cell_size, y * self.cell_size))
