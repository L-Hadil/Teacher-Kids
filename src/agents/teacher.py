import pygame


class Teacher:
    def __init__(self, x, y, cell_size, icon_path, number_of_kids, tick_delay):
        """
        Initialise la maîtresse.

        Args:
        - x (int): Position initiale en x (colonne).
        - y (int): Position initiale en y (ligne).
        - cell_size (int): Taille d'une cellule (en pixels).
        - icon_path (str): Chemin vers l'icône de la maîtresse.
        - number_of_kids (int): Nombre total d'enfants à surveiller.
        - tick_delay (int): Nombre de ticks à attendre entre chaque mouvement.
        """
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (cell_size, cell_size))
        self.number_of_kids = number_of_kids
        self.tick_delay = tick_delay  # Délai entre les mouvements (en ticks)
        self.tick_count = 0  # Compteur de ticks
        self.targets = []  # Liste des cibles actuelles
        self.score = 0  # Score de la maîtresse

    def move(self, environment, children_positions, children_states):
        """
        Déplace la maîtresse selon sa stratégie, en ignorant les enfants invisibles.

        Args:
        - environment (Environment): L'environnement du jeu.
        - children_positions (list): Liste des positions des enfants [(x, y), ...].
        - children_states (list): Liste des états des enfants (dictionnaire contenant "is_invisible").
        """
        self.targets = [
            (i, pos) for i, (pos, state) in enumerate(zip(children_positions, children_states))
            if not state["is_invisible"]  # Ignorer les enfants invisibles
               and not (environment.coloring_zone[0] <= pos[0] <= environment.coloring_zone[2] and
                        environment.coloring_zone[1] <= pos[1] <= environment.coloring_zone[3])
        ]

        if not self.targets:
            return  # Aucun enfant visible

        # Trouver la cible la plus proche
        closest_target = min(
            self.targets,
            key=lambda child: abs(self.x - child[1][0]) + abs(self.y - child[1][1])
        )

        # Se déplacer vers cette cible
        target_x, target_y = closest_target[1]
        self.move_towards(target_x, target_y)

    def move_towards(self, target_x, target_y):
        """
        Déplace la maîtresse vers une cible donnée.

        Args:
        - target_x (int): Colonne cible.
        - target_y (int): Ligne cible.
        """
        # Incrémenter le compteur de ticks
        self.tick_count += 1

        # Vérifier si la maîtresse peut bouger
        if self.tick_count >= self.tick_delay:
            self.tick_count = 0  # Réinitialiser le compteur
            # Calcul du déplacement
            if self.x < target_x:
                self.x += 1
            elif self.x > target_x:
                self.x -= 1

            if self.y < target_y:
                self.y += 1
            elif self.y > target_y:
                self.y -= 1

    def draw(self, screen):
        """
        Dessine la maîtresse à sa position actuelle.

        Args:
        - screen (pygame.Surface): Surface de jeu.
        """
        screen.blit(self.icon, (self.x * self.cell_size, self.y * self.cell_size))
