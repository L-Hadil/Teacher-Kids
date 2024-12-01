from src.agents.kid import Kid
from venv import logger
import math


class DistractorKid(Kid):
    DISTRACTION_RADIUS = 5  # Distance maximale pour rester en mode distraction
    FAR_DISTANCE_THRESHOLD = 8  # Distance à laquelle chercher des bonbons si la maîtresse est trop loin

    def __init__(self, x, y, cell_size, icon_path):
        """
        Initialise l'agent DistractorKid.

        Args:
        - x (int): Position initiale en x (colonne).
        - y (int): Position initiale en y (ligne).
        - cell_size (int): Taille d'une cellule (en pixels).
        - icon_path (str): Chemin vers l'icône de l'enfant.
        """
        super().__init__(x, y, cell_size, icon_path)
        self.distracting = True  # L'état où il cherche à distraire la maîtresse
        self.current_target = None  # Mémorise la cible actuelle
        self.last_position = (x, y)  # Pour détecter les blocages
        self.blocked_counter = 0  # Compteur pour détecter les blocages persistants

    def move(self, environment, teacher_position):
        """
        Stratégie : attirer la maîtresse tout en récupérant des bonbons si elle est éloignée.

        Args:
        - environment (Environment): L'environnement actuel.
        - teacher_position (tuple): Position de la maîtresse (x, y).
        """
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0  # Réinitialiser le compteur

        # Si l'agent a un bonbon, retourner à la position initiale
        if self.has_candy:
            if self.path_stack:
                self.x, self.y = self.path_stack.pop()
                logger.info(f"DistractorKid returning to initial position at ({self.x}, {self.y}).")

                if not self.path_stack:  # Si arrivé à la position initiale
                    self.has_candy = False
                    self.score += 1
                    logger.info(f"DistractorKid delivered candy and scored! Current score: {self.score}")
            return

        # Calculer la distance à la maîtresse
        distance_to_teacher = math.sqrt((self.x - teacher_position[0]) ** 2 + (self.y - teacher_position[1]) ** 2)

        # Priorité de la distraction
        if distance_to_teacher <= self.DISTRACTION_RADIUS:
            self.distracting = True
        elif distance_to_teacher > self.FAR_DISTANCE_THRESHOLD:
            self.distracting = False  # Chercher des bonbons si la maîtresse est très loin

        # Comportement basé sur l'état actuel
        if self.distracting:
            # Mode distraction : essayer de rester autour de la maîtresse
            self.current_target = self.calculate_distracting_position(environment, teacher_position)
            logger.info(f"DistractorKid distracting around teacher at target: {self.current_target}.")
        else:
            # Mode collecte de bonbons
            self.current_target = self.set_target(environment)
            logger.info(f"DistractorKid collecting candy at target: {self.current_target}.")

        # Enregistrer la position actuelle dans la pile avant de bouger
        if not self.has_candy:
            self.path_stack.append((self.x, self.y))

        # Déplacement vers la cible
        self.move_towards_target(self.current_target[0], self.current_target[1])

        # Vérifier les interactions avec les zones
        self.handle_candy_interactions(environment)

        # Détecter un blocage
        self.detect_and_handle_blockage()

    def calculate_distracting_position(self, environment, teacher_position):
        """
        Calcule une position stratégique pour attirer la maîtresse.

        Args:
        - environment (Environment): L'environnement actuel.
        - teacher_position (tuple): Position de la maîtresse (x, y).

        Returns:
        - (int, int): Coordonnées de la position cible.
        """
        # Rester proche de la maîtresse mais légèrement en mouvement
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in offsets:
            new_x = teacher_position[0] + dx
            new_y = teacher_position[1] + dy
            if 0 <= new_x < environment.width and 0 <= new_y < environment.height:
                return (new_x, new_y)

        # Fallback : rester exactement sur la maîtresse
        return teacher_position

    def move_towards_target(self, target_x, target_y):
        """
        Déplace DistractorKid vers une cible donnée.

        Args:
        - target_x (int): Colonne cible.
        - target_y (int): Ligne cible.
        """
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

        logger.info(f"DistractorKid moved towards ({target_x}, {target_y}) from ({self.x}, {self.y}).")

    def detect_and_handle_blockage(self):
        """
        Détecte et gère les blocages.
        """
        if self.last_position == (self.x, self.y):
            self.blocked_counter += 1
            if self.blocked_counter > 3:  # Considérer bloqué après 3 cycles consécutifs
                logger.warning(f"DistractorKid stuck at ({self.x}, {self.y}). Resetting to distraction mode.")
                self.distracting = True  # Revenir en mode distraction
                self.current_target = None  # Réinitialiser la cible
                self.blocked_counter = 0
        else:
            self.blocked_counter = 0  # Réinitialiser le compteur si l'agent bouge

        self.last_position = (self.x, self.y)  # Mettre à jour la dernière position
