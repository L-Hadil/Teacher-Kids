import random
import pygame
import logging

from src.agents.strategies.waitAndGo import WaitAndGo
from src.agents.teacher import Teacher
from src.agents.strategies.direct_to_candy import DirectToCandy
from src.agents.strategies.longestPath import LongestPath
from src.environment import Environment


class Game:
    def __init__(self, width, height, cell_size, candy_zone, coloring_zone, candy_count, candy_icon_path, teacher_icon_path, child1_icon_path, child2_icon_path, child3_icon_path):
        """
        Initialise le jeu.
        """
        pygame.init()

        self.screen_width = width * cell_size
        self.screen_height = height * cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height + 100))  # +100 pour la zone des scores
        pygame.display.set_caption("Candy Game Environment")
        self.clock = pygame.time.Clock()

        # Initialiser l'environnement
        self.environment = Environment(width, height, cell_size, candy_zone, coloring_zone, candy_count, candy_icon_path)

        # Initialiser les enfants et la maîtresse
        self.children = [
            DirectToCandy(3, 1, cell_size, child1_icon_path),  # Enfant 1
            LongestPath(4, 2, cell_size, child2_icon_path),  # Enfant 2
            WaitAndGo(2, 3, cell_size, child3_icon_path)  # Enfant 3
        ]

        self.teacher = Teacher(3, 2, cell_size, teacher_icon_path, number_of_kids=len(self.children), tick_delay=8)

        # Contrôle de la boucle principale
        self.running = True  # Initialisation de l'état du jeu

    def draw_score_area(self):
        """
        Dessine une zone en bas de la fenêtre pour afficher les scores.
        """
        # Dessiner un fond pour la zone des scores
        pygame.draw.rect(
            self.screen,
            (220, 220, 220),  # Couleur gris clair
            (0, self.environment.height * self.environment.cell_size, self.screen_width, 100)  # Zone des scores
        )

        # Afficher les scores des enfants
        font = pygame.font.Font(None, 30)  # Police pour le texte
        x_position = 10  # Position initiale en x
        y_position = self.environment.height * self.environment.cell_size + 10  # Position initiale en y

        for child in self.children:
            score_text = f"{type(child).__name__} Score: {child.score}"  # Texte à afficher
            text_surface = font.render(score_text, True, (0, 0, 0))  # Couleur noire pour le texte
            self.screen.blit(text_surface, (x_position, y_position))  # Afficher le texte à l'écran
            y_position += 30  # Décaler vers le bas pour le prochain score

    def check_interception(self):
        """Vérifie si la maîtresse intercepte un enfant."""
        for child in self.children:
            if (child.x, child.y) == (self.teacher.x, self.teacher.y):
                if child.has_candy:
                    # Si intercepté avec un bonbon
                    child.has_candy = False
                    self.environment.candy_count += 1  # Remettre le bonbon dans la zone
                    logger.info(f"Teacher caught {type(child).__name__} with a candy! Returning candy to the zone.")
                # Renvoyer l'enfant à sa position initiale
                child.x, child.y = child.initial_position
                child.path_stack.clear()  # Vider la pile pour réinitialiser le chemin
                logger.info(
                    f"{type(child).__name__} reset to initial position {child.initial_position} after being caught.")

    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Déplacer la maîtresse
            self.teacher.move(self.environment, [(child.x, child.y) for child in self.children])

            # Déplacer les enfants
            for child in self.children:
                all_kids_positions = [(c.x, c.y) for c in self.children if c != child]
                if isinstance(child, WaitAndGo):
                    child.move(self.environment, (self.teacher.x, self.teacher.y), all_kids_positions)
                else:
                    child.move(self.environment, (self.teacher.x, self.teacher.y))

            # Vérifier les interceptions
            self.check_interception()

            # Dessiner tout
            self.screen.fill((255, 255, 255))  # Fond blanc
            self.environment.draw(self.screen)
            self.teacher.draw(self.screen)
            for child in self.children:
                child.draw(self.screen)

            # Afficher les scores
            self.draw_score_area()

            # Rafraîchir l'écran
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("CandyGame")
