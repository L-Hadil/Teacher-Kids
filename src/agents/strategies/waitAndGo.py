from src.agents.kid import Kid

class WaitAndGo(Kid):
    def __init__(self, x, y, cell_size, icon_path):
        super().__init__(x, y, cell_size, icon_path)
        self.returned_to_base = False  # Indique si l'agent est déjà revenu à la base après un échec
        self.initial_position = (x, y)  # Sauvegarde de la position initiale avant le début du jeu

    def move(self, environment, teacher_position, all_kids_positions):
        """
        Stratégie "Wait and Go" : Prend des précautions avant de bouger.
        """
        teacher_x, teacher_y = teacher_position

        # Respecter le délai avant de bouger
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0  # Réinitialiser le compteur

        # Vérifier la fin de la punition
        self.check_punishment()
        if self.is_punished:
            return

        # Vérifier la fin de l'invisibilité
        self.check_invisibility()

        # Si l'agent retourne à la base (avec un bonbon ou après interception)
        if self.has_candy:
            target_x, target_y = self.initial_position
        else:
            target_x, target_y = self.set_target(environment)

        # Éviter la maîtresse si elle est proche
        if abs(self.x - teacher_x) + abs(self.y - teacher_y) <= 3:
            print(f"{type(self).__name__} is waiting for the teacher to move away.")
            return

        # Déplacer directement vers la cible
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

        # Si arrivé à la base avec un bonbon, marquer un point
        if (self.x, self.y) == self.initial_position and self.has_candy:
            self.has_candy = False
            self.score += 1
            print(f"{type(self).__name__} scored! Current score: {self.score}")

        # Gérer les interactions avec les bonbons
        self.handle_candy_interactions(environment)
