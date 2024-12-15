from collections import deque
from src.agents.kid import Kid
class DirectToTarget(Child):
    def __init__(self, x, y, cell_size, icon_path):
        super().__init__(x, y, cell_size, icon_path)

    def perform_move(self, environment, supervisor_position):
        """
        Stratégie "directe" : Aller directement vers la cible (bonbons ou zone de coloriage).
        """
        # Gestion du délai avant déplacement
        self.action_count += 1
        if self.action_count < Child.DEFAULT_ACTION_DELAY:
            return
        self.action_count = 0  # Réinitialiser le compteur

        # Si l'agent retourne à sa position initiale après avoir récupéré un objet
        if self.is_holding_item and self.movement_stack:
            self.x, self.y = self.movement_stack.pop()  # Retour via le chemin enregistré
            if not self.movement_stack:  # Si arrivé à la position initiale
                self.is_holding_item = False
                self.points += 1
            return

        # Déterminer la cible actuelle
        target_x, target_y = self.find_target(environment)

        # Enregistrer la position actuelle avant déplacement
        if not self.is_holding_item:
            self.movement_stack.append((self.x, self.y))

        # Mouvement direct vers la cible
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

        # Vérification des interactions avec les objets ou zones de l'environnement
        self.process_item_interactions(environment)
