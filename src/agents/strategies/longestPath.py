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
        Stratégie "chemin le plus long" : L'agent explore en suivant le chemin le plus long,
        récupère des bonbons et marque des points tout en prenant en compte les potions.
        """
        # Respecter le délai avant de bouger
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0  # Réinitialiser le compteur

        # Vérifier la fin de la punition
        self.check_punishment()

        # Vérifier la fin de l'invisibilité
        self.check_invisibility()

        # Si l'agent est puni, il ne bouge pas
        if self.is_punished:
            return

        # Réinitialiser `has_taken_potion` si l'effet d'invisibilité est terminé
        if not self.is_invisible:
            self.has_taken_potion = False

        # Vérifier si l'agent est à sa position initiale avec un bonbon
        if self.has_candy and (self.x, self.y) == self.initial_position:
            self.has_candy = False  # Déposer le bonbon
            self.score += 1  # Incrémenter le score
            self.path_stack.clear()  # Effacer le chemin précédent
            print(f"{type(self).__name__} scored a point! Current score: {self.score}")

            # Recalculer la cible après avoir marqué un point
            if environment.candy_count > 0:
                target_x, target_y = self.set_target(environment)  # Trouver un nouveau bonbon
                self.move_towards(target_x, target_y)
            return

        # Prioriser la potion si elle est disponible et pas encore prise
        if not self.has_taken_potion:
            nearest_potion = self.find_nearest_potion(environment)
            if nearest_potion:
                # Se déplacer vers la potion
                self.move_towards(nearest_potion[0], nearest_potion[1])
                self.handle_potion_interactions(environment)  # Ramasse la potion
                if self.is_invisible:  # Si la potion a été ramassée
                    self.has_taken_potion = True
                    self.path_stack.clear()  # Effacer le chemin précédent pour éviter un retour inutile

                    # Recalculer la stratégie : déterminer la prochaine cible
                    if not self.has_candy:
                        target_x, target_y = self.set_target(environment)  # Trouver un bonbon
                    else:
                        target_x, target_y = self.initial_position  # Retourner à la base
                    self.move_towards(target_x, target_y)  # Continuer immédiatement
                return

        # Déterminer la cible actuelle (zone de bonbons)
        target_x, target_y = self.set_target(environment)

        # Si l'agent est arrivé à la zone de bonbons, tenter de récupérer un bonbon
        if (self.x, self.y) == (target_x, target_y):
            if not self.has_candy and environment.candy_count > 0:
                self.has_candy = True  # Ramasser un bonbon
                environment.candy_count -= 1
                print(f"{type(self).__name__} picked a candy! Remaining candies: {environment.candy_count}")

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
