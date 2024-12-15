from src.agents.kid import Kid

class DirectToCandy(Kid):
    def __init__(self, x, y, cell_size, icon_path):
        super().__init__(x, y, cell_size, icon_path)
        self.returned_to_base = False  # Indique si l'agent est déjà revenu à la base après un échec
        self.has_taken_potion = False  # Indique si l'enfant a déjà pris une potion

    def move(self, environment, teacher_position):
        """
        Stratégie "directe" : Priorise la potion si disponible, puis cherche un bonbon.
        Utilise l'immunité pour ramasser un bonbon et marquer un point.
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

        # Prioriser la potion si elle est disponible et pas encore prise
        if not self.has_taken_potion:
            nearest_potion = self.find_nearest_potion(environment)
            if nearest_potion:
                self.move_towards(nearest_potion[0], nearest_potion[1])
                self.handle_potion_interactions(environment)  # Ramasse la potion
                if self.is_invisible:  # Si la potion a été ramassée
                    self.has_taken_potion = True
                return  # Continue directement depuis la position actuelle

        # Si l'agent retourne à sa case initiale (avec un bonbon ou après interception)
        if self.has_candy or self.returned_to_base and self.path_stack:
            self.x, self.y = self.path_stack.pop()  # Revenir en arrière via le chemin stocké
            if not self.path_stack and self.returned_to_base:  # Si arrivé à la position initiale après échec
                self.returned_to_base = True
            elif not self.path_stack and self.has_candy:  # Si arrivé à la position initiale avec un bonbon
                self.has_candy = False
                self.score += 1  # Marquer le point
                print(f"{type(self).__name__} scored a point! Current score: {self.score}")
            return

        # Vérifier si la zone de bonbons est vide
        if not self.has_candy and environment.candy_count == 0:
            # Préparer le retour en suivant le chemin inversé
            self.returned_to_base = True
            return

        # Déterminer la cible actuelle (bonbon ou coloriage)
        target_x, target_y = self.set_target(environment)

        # Enregistrer la position actuelle dans la pile avant de bouger (si utile)
        if not self.has_candy:
            self.path_stack.append((self.x, self.y))

        # Se déplacer directement vers la cible
        self.move_towards(target_x, target_y)

        # Vérifier les interactions avec la zone de bonbons
        self.handle_candy_interactions(environment)
