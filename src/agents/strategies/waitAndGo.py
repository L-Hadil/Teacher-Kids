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

        # Si l'agent retourne à sa case initiale (avec un bonbon ou après interception)
        if self.has_candy or (self.returned_to_base and self.path_stack):
            self.x, self.y = self.path_stack.pop()  # Revenir en arrière via le chemin stocké
            if not self.path_stack and self.returned_to_base:  # Si arrivé à la position initiale après échec
                self.returned_to_base = True
            elif not self.path_stack and self.has_candy:  # Si arrivé à la position initiale avec un bonbon
                self.has_candy = False
                self.score += 1
            return

        # Si l'agent est déjà revenu à la base après avoir trouvé la zone de bonbons vide
        if self.returned_to_base:
            return  # Ne plus sortir de la zone de coloriage

        # Attendre que la maîtresse soit loin (distance > 3)
        if abs(self.x - teacher_x) + abs(self.y - teacher_y) <= 3:
            return

        # Déterminer une cible détournée vers la zone de bonbons
        target_x, target_y = self.set_target(environment)

        # Si l'agent atteint la zone de bonbons mais qu'il n'y en a plus
        if (self.x, self.y) == (target_x, target_y) and not self.has_candy and environment.candy_count == 0:
            # Préparer le retour progressif avec chemin inverse
            self.returned_to_base = True
            self.path_stack.append((self.x, self.y))  # Ajouter la position actuelle à la pile
            return

        # Prendre un chemin détourné (augmenter X ou Y pour éviter un chemin direct)
        if not self.has_candy:
            if abs(self.x - target_x) > abs(self.y - target_y):
                if self.x < target_x:
                    self.path_stack.append((self.x + 1, self.y))
                else:
                    self.path_stack.append((self.x - 1, self.y))
            else:
                if self.y < target_y:
                    self.path_stack.append((self.x, self.y + 1))
                else:
                    self.path_stack.append((self.x, self.y - 1))
            self.path_stack.append((self.x, self.y))  # Enregistrer la position actuelle

        # Se déplacer vers la cible détournée
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

        # Vérifier les interactions avec les zones
        self.handle_candy_interactions(environment)
