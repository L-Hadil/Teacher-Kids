from src.agents.kid import Kid
from venv import logger


class WaitAndGo(Kid):
    def move(self, environment, teacher_position, all_kids_positions):
        """
        Stratégie "Wait and Go".
        """
        # Respecter le délai avant de bouger basé sur DEFAULT_TICK_DELAY
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0  # Réinitialiser le compteur

        # Si l'agent retourne à sa case initiale (avec un bonbon)
        if self.has_candy:
            if self.path_stack:
                # Revenir à la case précédente selon la pile
                self.x, self.y = self.path_stack.pop()
                logger.info(f"WaitAndGo is returning to initial position via ({self.x}, {self.y})")
            if not self.path_stack:  # Si arrivé à la position initiale
                self.has_candy = False
                self.score += 1
                logger.info(f"WaitAndGo delivered candy and scored! Current score: {self.score}")
            return

        # Vérifier si d'autres enfants sont encore dans la zone de coloriage
        others_in_coloring_zone = any(
            environment.coloring_zone[0] <= pos[0] <= environment.coloring_zone[2] and
            environment.coloring_zone[1] <= pos[1] <= environment.coloring_zone[3]
            for pos in all_kids_positions
        )
        if others_in_coloring_zone:
            logger.info(f"WaitAndGo is waiting for others to leave the coloring zone.")
            return

        # Déterminer la cible actuelle (zone de bonbons)
        target_x, target_y = self.set_target(environment)

        # Enregistrer la position actuelle dans la pile avant de bouger
        if not self.has_candy:
            self.path_stack.append((self.x, self.y))

        # Se déplacer directement vers la cible
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
