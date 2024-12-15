import math
from src.agents.kid import Kid



class DistractorKid(Kid):
    DISTRACTION_RADIUS = 5
    FAR_DISTANCE_THRESHOLD = 8

    def __init__(self, x, y, cell_size, icon_path):
        super().__init__(x, y, cell_size, icon_path)
        self.initial_position = (x, y)
        self.distracting = True
        self.current_target = None
        self.returned_to_base = False  # Indique si l'agent est déjà revenu à la base après un échec

    def move(self, environment, teacher_position):
        """
        Stratégie de distraction : Distraire la maîtresse ou chercher un bonbon.
        Recalcule dynamiquement le chemin après chaque étape importante.
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
            print(f"{type(self).__name__} scored a point! Current score: {self.score}")

            # Recalculer la cible après avoir marqué un point
            if environment.candy_count > 0:
                self.current_target = self.find_candy(environment)  # Trouver un nouveau bonbon
            else:
                self.current_target = None  # Aucune cible disponible
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

                    # Recalculer la stratégie : continuer la distraction ou chercher un bonbon
                    if self.distracting:
                        self.current_target = self.calculate_distracting_position(environment, teacher_position)
                    elif not self.has_candy:
                        self.current_target = self.find_candy(environment)
                    return
                return

        # Mode distraction ou collecte
        if self.distracting:
            self.current_target = self.calculate_distracting_position(environment, teacher_position)
        else:
            self.current_target = self.find_candy(environment)

        # Si aucune cible n'est trouvée
        if not self.current_target and not self.has_candy:
            self.return_to_coloring_zone(environment, teacher_position, back_to_base=True)
            return

        # Déplacement vers la cible
        if self.current_target:
            self.move_towards_target(*self.current_target)

        # Gérer les interactions avec les bonbons
        self.handle_candy_interactions(environment)

    def find_candy(self, environment):
        """
        Trouve la position d'un bonbon disponible dans la zone des bonbons.
        """
        for x in range(environment.candy_zone[0], environment.candy_zone[2] + 1):
            for y in range(environment.candy_zone[1], environment.candy_zone[3] + 1):
                if environment.is_candy_at(x, y):
                    return (x, y)
        return None

    def calculate_longest_path_to_target(self, target, teacher_position, environment):
        """
        Calcule un chemin vers la cible (position initiale) tout en maximisant la distance avec la maîtresse.
        """
        paths = self.find_all_paths(self.x, self.y, target, environment)
        if not paths:
            return []
        farthest_path = max(
            paths, key=lambda path: self.calculate_path_distance_from_teacher(path, teacher_position)
        )
        return farthest_path

    def calculate_path_distance_from_teacher(self, path, teacher_position):
        """
        Calcule la distance moyenne d'un chemin par rapport à la position de la maîtresse.
        """
        return sum(
            math.sqrt((x - teacher_position[0]) ** 2 + (y - teacher_position[1]) ** 2)
            for x, y in path
        ) / len(path)

    def find_all_paths(self, start_x, start_y, target, environment):
        """
        Trouve tous les chemins possibles entre deux points.
        Utilise une recherche simple pour retourner plusieurs chemins.
        """
        # Implémentez une recherche en largeur ou une méthode DFS ici
        pass

    def calculate_distracting_position(self, environment, teacher_position):
        """
        Calcule une position proche de la maîtresse pour la distraire.
        """
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in offsets:
            new_x = teacher_position[0] + dx
            new_y = teacher_position[1] + dy
            if 0 <= new_x < environment.width and 0 <= new_y < environment.height:
                return (new_x, new_y)
        return teacher_position

    def move_towards_target(self, target_x, target_y):
        """
        Déplace l'agent vers la cible donnée.
        """
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1
