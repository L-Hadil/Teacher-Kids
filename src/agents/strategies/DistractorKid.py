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
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0

        # Si l'agent a un bonbon, il retourne à sa position initiale
        if self.has_candy:
            self.return_to_coloring_zone(environment, teacher_position)
            return

        # Si l'agent est déjà revenu à la base après avoir trouvé la zone de bonbons vide
        if self.returned_to_base:
            return  # Rester dans la zone de coloriage

        # Déterminer la distance à la maîtresse
        distance_to_teacher = math.sqrt(
            (self.x - teacher_position[0]) ** 2 + (self.y - teacher_position[1]) ** 2
        )

        # Définir le mode (distraction ou collecte de bonbons)
        if distance_to_teacher <= self.DISTRACTION_RADIUS:
            self.distracting = True
        elif distance_to_teacher > self.FAR_DISTANCE_THRESHOLD:
            self.distracting = False

        # Comportement basé sur le mode
        if self.distracting:
            self.current_target = self.calculate_distracting_position(environment, teacher_position)
        else:
            self.current_target = self.find_candy(environment)

        # Si la zone de bonbons est vide et il n'y a pas de cible
        if not self.has_candy and not self.current_target and environment.candy_count == 0:
            self.return_to_coloring_zone(environment, teacher_position, back_to_base=True)
            return

        # Déplacement vers la cible
        if self.current_target:
            self.move_towards_target(*self.current_target)

        # Gérer les interactions avec les bonbons
        self.handle_candy_interactions(environment)

    def return_to_coloring_zone(self, environment, teacher_position, back_to_base=False):
        """
        Retourne à la position initiale tout en maximisant la distance avec la maîtresse
        ou revient progressivement après avoir trouvé la zone de bonbons vide.
        """
        if back_to_base:
            if self.path_stack:
                self.x, self.y = self.path_stack.pop()
                if not self.path_stack:  # Une fois revenu à la position initiale
                    self.returned_to_base = True
            return

        farthest_path = self.calculate_longest_path_to_target(
            self.initial_position, teacher_position, environment
        )
        if farthest_path:
            next_position = farthest_path.pop(0)
            self.x, self.y = next_position


        if (self.x, self.y) == self.initial_position:
            self.has_candy = False
            self.score += 1

            self.distracting = True  # Reprendre la distraction après marquer un point

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
