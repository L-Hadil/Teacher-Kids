


import random
import pygame
import logging

from src.agents.strategies.waitAndGo import WaitAndGo
from src.agents.teacher import Teacher
from src.agents.strategies.direct_to_candy import DirectToCandy
from src.agents.strategies.longestPath import LongestPath
from src.agents.strategies.DistractorKid import DistractorKid
from src.environment import Environment
from src.agents.strategies.bfs import bfs

class Game:
    def __init__(self, width, height, cell_size, candy_zone, coloring_zone, candy_count, candy_icon_path, teacher_icon_path, child1_icon_path, child2_icon_path, child3_icon_path, child4_icon_path, child5_icon_path, game_duration):
        """
        Initialise le jeu.
        """
        pygame.init()

        self.screen_width = width * cell_size
        self.screen_height = height * cell_size + 300  # +100 pour la zone des scores
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Candy Game Environment")
        self.clock = pygame.time.Clock()

        # Initialiser l'environnement
        self.environment = Environment(width, height, cell_size, candy_zone, coloring_zone, candy_count, candy_icon_path)
        self.game_duration = game_duration  # Durée totale en secondes
        self.start_time = None  # Temps de début
        self.screen_height = height * cell_size + 800  # Hauteur totale ajustée pour la grande zone

        # Initialiser les enfants et la maîtresse
        self.children = [
            DirectToCandy(2, 1, cell_size, child1_icon_path),
            LongestPath(2, 2, cell_size, child2_icon_path),
            WaitAndGo(3, 3, cell_size, child3_icon_path),
            DistractorKid(4, 3, cell_size, child4_icon_path),
            bfs(3, 2, cell_size, child5_icon_path),
            bfs(4, 2, cell_size, child5_icon_path),
            LongestPath(4, 1, cell_size, child2_icon_path)
        ]

        self.teacher = Teacher(6, 3, cell_size, teacher_icon_path, number_of_kids=len(self.children), tick_delay=8)

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
        Dessine une zone beaucoup plus grande en bas de la fenêtre pour afficher les scores,
        le temps restant, et prévoir de l'espace pour des informations futures.
        """
        # Hauteur très grande de la zone des scores : 800 pixels
        score_area_height = 800
        pygame.draw.rect(
            self.screen,
            (220, 220, 220),  # Couleur gris clair
            (0, self.environment.height * self.environment.cell_size, self.screen_width, score_area_height)
        )

        font = pygame.font.Font(None, 25)  # Taille de police standard
        x_position = 10  # Position X pour les scores
        y_position = self.environment.height * self.environment.cell_size + 10  # Position Y initiale
        line_spacing = 30  # Espacement entre les lignes

        # 1. Afficher les scores pour chaque enfant
        for child in self.children:
            score_text = f"{type(child).__name__} Score: {child.score}"
            text_surface = font.render(score_text, True, (0, 0, 0))  # Texte noir
            self.screen.blit(text_surface, (x_position, y_position))
            y_position += line_spacing  # Ajouter un espacement entre les lignes

        # 2. Afficher le score de la maîtresse
        teacher_score_text = f"Teacher Score: {self.teacher.score}"
        teacher_score_surface = font.render(teacher_score_text, True, (0, 0, 255))  # Texte bleu
        self.screen.blit(teacher_score_surface, (x_position, y_position))
        y_position += line_spacing

        # 3. Afficher le nombre de bonbons restants
        candies_text = f"Candies Remaining: {self.environment.candy_count}"
        candies_surface = font.render(candies_text, True, (0, 0, 0))  # Texte noir
        self.screen.blit(candies_surface, (x_position, y_position))
        y_position += line_spacing  # Ajouter un espacement pour le texte suivant

        # 4. Calculer et afficher le temps restant à droite
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Temps écoulé en secondes
        remaining_time = max(0, self.game_duration - elapsed_time)  # Éviter les valeurs négatives
        time_text = f"Time Remaining: {int(remaining_time)}s"
        time_surface = font.render(time_text, True, (255, 0, 0))  # Texte rouge pour le temps restant
        time_x_position = self.screen_width - time_surface.get_width() - 10  # Aligner à droite
        self.screen.blit(time_surface, (
            time_x_position, self.environment.height * self.environment.cell_size + 10))  # Même hauteur que les scores

    def determine_winner(self):
        """Détermine le gagnant en fonction des scores."""
        # Find the maximum score
        max_score = max(child.score for child in self.children)

        # Find all children who have the maximum score
        winners = [child for child in self.children if child.score == max_score]

        if len(winners) > 1:
            # There is a tie
            winner_names = ", ".join([type(child).__name__ for child in winners])
            logger.warning(f"Game Over! It's a tie between: {winner_names} with {max_score} candies collected each.")
            print(f"Game Over! It's a tie between: {winner_names} with {max_score} candies collected each.")
        else:
            # There is a single winner
            winner = winners[0]
            logger.warning(f"Game Over! Winner: {type(winner).__name__} with {winner.score} candies collected.")
            print(f"Game Over! Winner: {type(winner).__name__} with {winner.score} candies collected.")

    def check_interception(self):
        """Vérifie si la maîtresse intercepte un enfant."""
        for child in self.children:
            if (child.x, child.y) == (self.teacher.x, self.teacher.y):
                child.interception_count += 1  # Incrémenter le compteur d'interceptions
                if child.interception_count > 5:
                    child.punish()  # Punir l'enfant s'il est intercepté plus de 5 fois
                    logger.warning(f"{type(child).__name__} is punished for too many interceptions!")
                else:
                    if child.has_candy:
                        # Si intercepté avec un bonbon
                        child.has_candy = False
                        self.environment.candy_count += 1  # Remettre le bonbon dans la zone
                        self.teacher.score += 1  # Incrémenter le score de la maîtresse
                        logger.warning(f"Teacher caught {type(child).__name__} with a candy!")
                    # Renvoyer l'enfant à sa position initiale
                    child.x, child.y = child.initial_position
                    child.path_stack.clear()  # Vider la pile pour réinitialiser le chemin

    def run(self):
        """Boucle principale du jeu."""
        self.start_time = pygame.time.get_ticks()  # Temps de départ en millisecondes

        self.observe_initial_state()
        logger.info("Starting the game: Kids and teacher begin their actions!")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convertir en secondes
            if elapsed_time >= self.game_duration:
                self.determine_winner()  # Déterminer le gagnant
                logger.warning("Time's up! The game is over.")
                self.running = False
                continue

            # Déplacer la maîtresse
            self.teacher.move(self.environment, [(child.x, child.y) for child in self.children])

            # Déplacer les enfants
            for child in self.children:
                child.check_punishment()  # Vérifier si la punition est terminée
                if not child.is_punished:
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

            # Afficher les scores et le temps restant
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