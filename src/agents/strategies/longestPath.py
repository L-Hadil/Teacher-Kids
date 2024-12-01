from src.agents.kid import Kid
from venv import logger

class LongestPath(Kid):
    def __init__(self, x, y, cell_size, icon_path):
        """
        Initialise l'agent LongestPath avec une pile pour enregistrer le chemin parcouru.

        Args:
        - x (int): Position initiale en x (colonne).
        - y (int): Position initiale en y (ligne).
        - cell_size (int): Taille d'une cellule (en pixels).
        - icon_path (str): Chemin vers l'icône de l'enfant.
        """
        super().__init__(x, y, cell_size, icon_path)

    def move(self, environment, teacher_position):
        """
        Stratégie "chemin le plus long".
        """
        initial_position = (self.x, self.y)

        # Respecter le délai avant de bouger basé sur DEFAULT_TICK_DELAY
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0  # Réinitialiser le compteur

        # Si l'agent retourne à sa case initiale (avec un bonbon ou après interception)
        if self.has_candy:
            self.handle_candy_interactions(environment)
            return

        # Déterminer la cible actuelle
        target_x, target_y = self.set_target(environment)

        # Enregistrer la position actuelle dans la pile avant de se déplacer
        if not self.has_candy:
            self.path_stack.append((self.x, self.y))

        # Priorité au déplacement horizontal
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1
        elif self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

        # Vérifier les interactions avec les zones
        self.handle_candy_interactions(environment)

        # Log des déplacements
        logger.info(f"LongestPath moved from {initial_position} to ({self.x}, {self.y}), target ({target_x}, {target_y})")
