import pygame
from environment import Environment


class Game:
    def __init__(self, width, height, cell_size, candy_zone, coloring_zone, candy_count, candy_icon_path):
        """
        Initialise le jeu et l'environnement.

        Args:
        - width (int): Largeur de la grille (en cellules).
        - height (int): Hauteur de la grille (en cellules).
        - cell_size (int): Taille d'une cellule (en pixels).
        - candy_zone (tuple): Coordonnées de la zone des bonbons.
        - coloring_zone (tuple): Coordonnées de la zone de coloriage.
        - candy_count (int): Nombre initial de bonbons disponibles.
        - candy_icon_path (str): Chemin vers l'icône des bonbons.
        """
        pygame.init()

        self.screen_width = width * cell_size
        self.screen_height = height * cell_size

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Candy Game Environment")
        self.clock = pygame.time.Clock()


        self.environment = Environment(width, height, cell_size, candy_zone, coloring_zone, candy_count, candy_icon_path)
        self.running = True

    def run(self):
        """Lance la boucle principale du jeu."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Effacer l'écran
            self.screen.fill((255, 255, 255))  # Fond blanc

            # Dessiner l'environnement
            self.environment.draw(self.screen)

            # Mettre à jour l'affichage
            pygame.display.flip()

            # Limiter à 30 FPS
            self.clock.tick(30)

        pygame.quit()
