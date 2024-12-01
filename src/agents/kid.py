import pygame
from abc import ABC, abstractmethod
from venv import logger

class Kid(ABC):
    DEFAULT_TICK_DELAY = 10  # Vitesse par défaut pour tous les enfants

    def __init__(self, x, y, cell_size, icon_path):
        """
        Initialise un enfant avec des comportements communs, incluant la gestion de vitesse.
        """
        self.x = x
        self.y = y
        self.initial_position = (x, y)  # Position initiale
        self.path_stack = []  # Pile pour enregistrer le chemin
        self.cell_size = cell_size
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (cell_size, cell_size))
        self.has_candy = False
        self.score = 0  # Score de l'enfant
        self.tick_count = 0  # Compteur pour gérer le délai

    def move(self, environment, teacher_position):
        """
        Contrôle le mouvement en respectant la vitesse fixée par DEFAULT_TICK_DELAY.
        """
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return  # Attendre

        self.tick_count = 0  # Réinitialiser le compteur

        # Logique de déplacement spécifique à chaque enfant
        self.x += 1  # Exemple : se déplacer d'une case à droite

    def set_target(self, environment):
        """
        Détermine la cible actuelle de l'enfant.
        """
        if self.has_candy:
            # Retourner à la zone coloriage en suivant le chemin inverse
            if self.path_stack:
                return self.path_stack[-1]
            else:
                logger.warning(f"{type(self).__name__} path_stack is empty. Returning to initial position.")
                return self.initial_position
        else:
            # Aller à la zone des bonbons
            target_x = (environment.candy_zone[0] + environment.candy_zone[2]) // 2
            target_y = (environment.candy_zone[1] + environment.candy_zone[3]) // 2
            return target_x, target_y

    def handle_candy_interactions(self, environment):
        """
        Gère les interactions de l'enfant avec la zone de bonbons et de coloriage.
        """
        if self.has_candy and self.path_stack and (self.x, self.y) == self.path_stack[-1]:
            self.path_stack.pop()  # Revenir via le chemin inverse
            if not self.path_stack:  # Arrivé à la position initiale
                self.has_candy = False
                self.score += 1
                logger.info(f"{type(self).__name__} delivered candy and scored! Current score: {self.score}")

        elif not self.has_candy and (self.x, self.y) == self.set_target(environment):
            if environment.candy_count > 0:
                self.has_candy = True
                environment.candy_count -= 1
                logger.info(f"{type(self).__name__} picked a candy at ({self.x}, {self.y}). Remaining candies: {environment.candy_count}")

    def draw(self, screen):
        """
        Dessine l'enfant sur l'écran.
        """
        screen.blit(self.icon, (self.x * self.cell_size, self.y * self.cell_size))
