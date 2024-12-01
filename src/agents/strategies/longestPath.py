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

        # Si l'agent retourne à sa case initiale (après avoir pris un bonbon)
        if self.has_candy:
            if self.path_stack:
                self.x, self.y = self.path_stack.pop()  # Revenir en suivant le chemin inverse

            if not self.path_stack:  # Si arrivé à la position initiale
                self.has_candy = False
                self.score += 1

            return

        # Déterminer la cible actuelle (zone de bonbons)
        target_x, target_y = self.set_target(environment)

        # Si l'agent est arrivé à la zone de bonbons, tenter de récupérer un bonbon
        if (self.x, self.y) == (target_x, target_y):
            if not self.has_candy and environment.candy_count > 0:
                self.has_candy = True
                environment.candy_count -= 1

            elif not self.has_candy:
                # Aucun bonbon disponible, retour à la zone initiale

                self.path_stack.append((self.x, self.y))  # Ajouter la position actuelle comme début du retour
                return

        # Enregistrer la position actuelle dans la pile avant de bouger
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


