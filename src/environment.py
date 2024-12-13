import pygame

class Environment:
    def __init__(self, width, height, cell_size, candy_zone, coloring_zone, candy_count, candy_icon_path):
        """
        Initialise l'environnement avec des bonbons et une zone de coloriage.
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.candy_zone = candy_zone
        self.coloring_zone = coloring_zone
        self.candy_count = candy_count
        self.candy_icon = pygame.image.load(candy_icon_path)  # Charger l'icône
        self.candy_icon = pygame.transform.scale(self.candy_icon, (cell_size, cell_size))  # Redimensionner
        self.agents_positions = []  # Liste des positions des agents dans la zone de coloriage

    def is_candy_at(self, x, y):
        """
        Vérifie si un bonbon est présent à une position donnée.

        Args:
        - x (int): Position X.
        - y (int): Position Y.

        Returns:
        - bool: True si un bonbon est présent, False sinon.
        """
        return (self.candy_zone[0] <= x <= self.candy_zone[2] and
                self.candy_zone[1] <= y <= self.candy_zone[3] and
                self.candy_count > 0)


    def is_in_coloring_zone(self, x, y):
        """
        Vérifie si une position est dans la zone de coloriage.

        Args:
        - x (int): Position X.
        - y (int): Position Y.

        Returns:
        - bool: True si la position est dans la zone de coloriage, sinon False.
        """
        return (self.coloring_zone[0] <= x <= self.coloring_zone[2] and
                self.coloring_zone[1] <= y <= self.coloring_zone[3])

    def add_agent_to_coloring_zone(self, x, y):
        """
        Ajoute un agent dans la zone de coloriage si la position est libre.

        Args:
        - x (int): Position X.
        - y (int): Position Y.

        Returns:
        - bool: True si l'agent a été ajouté, False sinon.
        """
        if self.is_in_coloring_zone(x, y) and (x, y) not in self.agents_positions:
            self.agents_positions.append((x, y))
            return True
        return False

    def remove_agent_from_coloring_zone(self, x, y):
        """
        Supprime un agent de la zone de coloriage.

        Args:
        - x (int): Position X.
        - y (int): Position Y.

        Returns:
        - bool: True si l'agent a été retiré, False sinon.
        """
        if (x, y) in self.agents_positions:
            self.agents_positions.remove((x, y))
            return True
        return False

    def draw(self, screen):
        """
        Dessine la grille, les zones et les bonbons.
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