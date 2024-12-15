import pygame
from abc import ABC


class Kid(ABC):
    DEFAULT_TICK_DELAY = 10  # Vitesse par défaut pour tous les enfants
    PUNISHMENT_DURATION = 5000  # Durée de punition en millisecondes (5 secondes)
    INVISIBILITY_DURATION = 10000  # Durée de l'invisibilité en millisecondes (10 secondes)

    def __init__(self, x, y, cell_size, icon_path):
        """
        Initialise un enfant avec des comportements communs, incluant la gestion de vitesse.
        """
        self.x = x
        self.y = y
        self.initial_position = (x, y)  # Position initiale
        self.path_stack = []  # Pile pour enregistrer le chemin
        self.cell_size = cell_size
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (cell_size, cell_size))
        self.has_candy = False  # Indique si l'enfant transporte un bonbon
        self.score = 0  # Score de l'enfant
        self.tick_count = 0  # Compteur pour gérer le délai de déplacement
        self.interception_count = 0  # Compteur d'interceptions
        self.punishment_start_time = None  # Temps de début de punition
        self.is_punished = False  # Indique si l'enfant est puni

        # Gestion de l'invisibilité
        self.is_invisible = False  # Indique si l'enfant est invisible
        self.invisibility_start_time = None  # Temps de début d'invisibilité

    def move(self, environment, teacher_position):
        """
        Contrôle le mouvement en respectant la vitesse fixée par DEFAULT_TICK_DELAY.
        Si l'enfant est puni ou invisible, il ne bouge pas.
        """
        # Vérifier la fin de la punition
        self.check_punishment()

        # Vérifier la fin de l'invisibilité
        self.check_invisibility()

        # Si l'enfant est puni, il ne bouge pas
        if self.is_punished:
            return

        # Gestion normale du mouvement avec un délai
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0  # Réinitialiser le compteur

    def handle_potion_interactions(self, environment):
        """
        Vérifie et applique l'effet de la potion si l'enfant la ramasse.
        """
        potion = environment.is_potion_at(self.x, self.y)
        if potion:
            self.become_invisible()  # Activer l'effet d'invisibilité
            self.path_stack.clear()  # Effacer le chemin stocké pour éviter tout retour inutile
            environment.collect_potion(self.x, self.y)  # Retirer la potion
            print(f"{type(self).__name__} ate a potion and became invisible!")

    def become_invisible(self):
        """
        Active l'invisibilité pour l'enfant.
        """
        self.is_invisible = True
        self.invisibility_start_time = pygame.time.get_ticks()
        print(f"{type(self).__name__} is now invisible!")

    def check_invisibility(self):
        """
        Désactive l'invisibilité après la durée définie.
        """
        if self.is_invisible and pygame.time.get_ticks() - self.invisibility_start_time >= Kid.INVISIBILITY_DURATION:
            self.is_invisible = False
            print(f"{type(self).__name__} is no longer invisible!")

    def punish(self):
        """
        Active la punition pour l'enfant.
        """
        self.is_punished = True
        self.punishment_start_time = pygame.time.get_ticks()  # Temps de début de la punition
        self.x, self.y = self.initial_position  # Retour à la position initiale
        self.path_stack.clear()  # Réinitialiser le chemin
        print(f"{type(self).__name__} is punished and will freeze for {Kid.PUNISHMENT_DURATION // 1000} seconds!")

    def check_punishment(self):
        """
        Vérifie si la punition est terminée.
        """
        if self.is_punished and pygame.time.get_ticks() - self.punishment_start_time >= Kid.PUNISHMENT_DURATION:
            self.is_punished = False
            self.interception_count = 0  # Réinitialiser le compteur d'interceptions
            print(f"{type(self).__name__} punishment is over and can move again!")

    def set_target(self, environment):
        """
        Détermine la cible actuelle de l'enfant.

        Args:
        - environment (Environment): L'environnement de jeu.

        Returns:
        - tuple: Les coordonnées (x, y) de la cible.
        """
        if self.has_candy:
            # Retourner à la zone de coloriage en suivant le chemin inverse
            if self.path_stack:
                return self.path_stack[-1]
            else:
                print(f"{type(self).__name__} path_stack is empty. Returning to initial position.")
                return self.initial_position
        else:
            # Aller à la zone des bonbons
            target_x = (environment.candy_zone[0] + environment.candy_zone[2]) // 2
            target_y = (environment.candy_zone[1] + environment.candy_zone[3]) // 2
            return target_x, target_y

    def draw(self, screen):
        """
        Dessine l'enfant sur l'écran. Change d'apparence si invisible.
        """
        if not self.is_invisible:
            screen.blit(self.icon, (self.x * self.cell_size, self.y * self.cell_size))
        else:
            # Dessiner un rectangle vert autour de l'enfant pour montrer qu'il est immunisé
            rect = pygame.Rect(self.x * self.cell_size, self.y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, (0, 255, 0), rect, 3)  # Vert avec une bordure de 3 pixels
            screen.blit(self.icon, (self.x * self.cell_size, self.y * self.cell_size))

    def find_nearest_potion(self, environment):
        """
        Trouve la potion active la plus proche.

        Args:
        - environment (Environment): L'environnement du jeu.

        Returns:
        - tuple: Coordonnées (x, y) de la potion la plus proche, ou None si aucune potion active.
        """
        nearest_potion = None
        nearest_distance = float('inf')
        for potion in environment.potions:
            if potion["active"]:  # Vérifie si la potion est active
                distance = abs(self.x - potion["position"][0]) + abs(self.y - potion["position"][1])
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_potion = potion["position"]
        return nearest_potion

    def move_towards(self, target_x, target_y):
        """
        Déplace l'enfant d'une étape vers une cible donnée.

        Args:
        - target_x (int): Coordonnée X de la cible.
        - target_y (int): Coordonnée Y de la cible.
        """
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

    def handle_candy_interactions(self, environment):
        """
        Gère les interactions de l'enfant avec la zone de bonbons.

        Args:
        - environment (Environment): L'environnement de jeu.
        """
        if not self.has_candy and environment.is_candy_at(self.x, self.y):
            # Ramasser un bonbon
            if environment.candy_count > 0:
                self.has_candy = True
                environment.candy_count -= 1
                print(f"{type(self).__name__} picked a candy! Remaining candies: {environment.candy_count}")

        elif self.has_candy and (self.x, self.y) == self.initial_position:
            # Retourner à la position initiale avec un bonbon pour marquer un point
            self.has_candy = False
            self.score += 1
            print(f"{type(self).__name__} scored a point! Current score: {self.score}")
