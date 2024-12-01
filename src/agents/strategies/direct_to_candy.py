from src.agents.kid import Kid
from venv import logger

class DirectToCandy(Kid):
    def __init__(self, x, y, cell_size, icon_path):
        super().__init__(x, y, cell_size, icon_path)

    def move(self, environment, teacher_position):
        """
        Stratégie "directe" : Aller directement à la cible (bonbons ou coloriage).
        """
        # Respecter le délai avant de bouger
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0  # Réinitialiser le compteur

        # Si l'agent retourne à sa case initiale (avec un bonbon ou après interception)
        if self.has_candy and self.path_stack:
            self.x, self.y = self.path_stack.pop()  # Revenir en arrière via le chemin stocké
            if not self.path_stack:  # Si arrivé à la position initiale
                self.has_candy = False
                self.score += 1
                logger.info(f"DirectToCandy delivered candy and scored! Current score: {self.score}")
            return

        # Déterminer la cible actuelle
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

        # Vérifier les interactions avec la zone de bonbons
        self.handle_candy_interactions(environment)
