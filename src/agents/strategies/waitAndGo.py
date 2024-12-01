from src.agents.kid import Kid
from venv import logger

class WaitAndGo(Kid):
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

        # Si l'agent retourne à sa case initiale (avec un bonbon)
        if self.has_candy:
            if self.path_stack:
                self.x, self.y = self.path_stack.pop()
                logger.info(f"WaitAndGo is returning to initial position via ({self.x}, {self.y})")
            if not self.path_stack:  # Si arrivé à la position initiale
                self.has_candy = False
                self.score += 1
                logger.info(f"WaitAndGo delivered candy and scored! Current score: {self.score}")
            return

        # Attendre que la maîtresse soit loin (distance > 3)
        if abs(self.x - teacher_x) + abs(self.y - teacher_y) <= 3:
            logger.info("WaitAndGo is waiting for the teacher to move further away.")
            return

        # Déterminer une cible détournée vers la zone de bonbons
        target_x, target_y = self.set_target(environment)
        if not self.has_candy:
            # Prendre un chemin détourné (augmenter X ou Y pour éviter un chemin direct)
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
