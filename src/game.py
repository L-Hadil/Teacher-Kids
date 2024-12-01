import random
import pygame
import logging

from src.agents.strategies.waitAndGo import WaitAndGo
from src.agents.teacher import Teacher
from src.agents.strategies.direct_to_candy import DirectToCandy
from src.agents.strategies.longestPath import LongestPath
from src.agents.strategies.DistractorKid import DistractorKid
from src.environment import Environment


class Game:
    def __init__(self, width, height, cell_size, candy_zone, coloring_zone, candy_count, candy_icon_path, teacher_icon_path, child1_icon_path, child2_icon_path, child3_icon_path, child4_icon_path):
        """
        Initialise le jeu.
        """
        pygame.init()

        self.screen_width = width * cell_size
        self.screen_height = height * cell_size + 100  # +100 pour la zone des scores
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Candy Game Environment")
        self.clock = pygame.time.Clock()

        # Initialiser l'environnement
        self.environment = Environment(width, height, cell_size, candy_zone, coloring_zone, candy_count, candy_icon_path)

        # Initialiser les enfants et la maîtresse
        self.children = [
            DirectToCandy(2, 1, cell_size, child1_icon_path),
            LongestPath(2, 2, cell_size, child2_icon_path),
            WaitAndGo(3, 3, cell_size, child3_icon_path),
            DistractorKid(4, 3, cell_size, child4_icon_path)
        ]

        self.teacher = Teacher(2, 3, cell_size, teacher_icon_path, number_of_kids=len(self.children), tick_delay=8)

        # Contrôle de la boucle principale
        self.running = True  # Initialisation de l'état du jeu

    def observe_initial_state(self, observation_time=3):
        """
        Permet au joueur d'observer l'état initial avant le début de la partie.

        Args:
        - observation_time (int): Durée en secondes pour afficher l'état initial.
        """
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < observation_time * 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            # Dessiner l'état initial
            self.screen.fill((255, 255, 255))  # Fond blanc
            self.environment.draw(self.screen)
            self.teacher.draw(self.screen)
            for child in self.children:
                child.draw(self.screen)
            self.draw_score_area()
            pygame.display.flip()
            self.clock.tick(30)

        logger.info("Initial observation completed. Starting game...")

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

        font = pygame.font.Font(None, 25)  # Police légèrement plus petite pour éviter les chevauchements
        x_position = 10  # Position initiale en x
        y_position = self.environment.height * self.environment.cell_size + 10  # Position initiale en y
        line_spacing = 20  # Espacement entre les lignes

        # Affichage des scores pour chaque enfant
        for i, child in enumerate(self.children):
            score_text = f"{type(child).__name__} Score: {child.score}"
            text_surface = font.render(score_text, True, (0, 0, 0))  # Couleur noire pour le texte
            self.screen.blit(text_surface, (x_position, y_position))
            y_position += line_spacing  # Ajouter de l'espace entre chaque ligne

        # Afficher le nombre de bonbons restants
        candies_text = f"Candies Remaining: {self.environment.candy_count}"
        candies_surface = font.render(candies_text, True, (0, 0, 0))  # Couleur noire pour le texte
        self.screen.blit(candies_surface, (x_position, y_position + 10))  # Affichage après les scores des enfants

    def check_interception(self):
        """Vérifie si la maîtresse intercepte un enfant."""
        for child in self.children:
            if (child.x, child.y) == (self.teacher.x, self.teacher.y):
                if child.has_candy:
                    # Si intercepté avec un bonbon
                    child.has_candy = False
                    self.environment.candy_count += 1  # Remettre le bonbon dans la zone
                    logger.warning(f"Teacher caught {type(child).__name__} with a candy!")
                # Renvoyer l'enfant à sa position initiale
                child.x, child.y = child.initial_position
                child.path_stack.clear()  # Vider la pile pour réinitialiser le chemin
                logger.info(f"{type(child).__name__} reset to initial position.")

    def determine_winner(self):
        """Détermine le gagnant en fonction des scores."""
        winner = max(self.children, key=lambda child: child.score)
        logger.warning(f"Game Over! Winner: {type(winner).__name__} with {winner.score} candies collected.")
        print(f"Game Over! Winner: {type(winner).__name__} with {winner.score} candies collected.")

    def run(self):
        """Boucle principale du jeu."""
        # Observer l'état initial
        self.observe_initial_state()

        logger.info("Starting the game: Kids and teacher begin their actions!")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Vérifier si le jeu doit s'arrêter
            if self.environment.candy_count == 0:
                self.determine_winner()
                self.running = False
                continue

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
    level=logging.INFO,  # Log niveau INFO pour suivre le jeu
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("CandyGame")
