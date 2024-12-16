from collections import deque
from src.agents.kid import Kid

class BFS(Kid):
    def __init__(self, x, y, cell_size, icon_path):
        super().__init__(x, y, cell_size, icon_path)
        self.path_stack = deque()  # Initialise une deque pour les déplacements
        self.initial_position = (x, y)  # Position initiale

    def bfs(self, start, target, environment):
        """
        Effectue une recherche en largeur (BFS) pour trouver le chemin le plus court vers la cible.

        Args:
        - start (tuple): Position de départ (x, y)
        - target (tuple): Position cible (x, y)
        - environment (Environment): L'environnement du jeu

        Returns:
        - list: Chemin le plus court sous forme de liste de (x, y)
        """
        queue = deque([(start, [start])])  # Initialise la file pour BFS
        visited = set()

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == target:
                return path

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < environment.width and 0 <= ny < environment.height and
                        (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

        return []  # Aucun chemin trouvé

    def move(self, environment, teacher_position):
        """
        Déplace l'agent en utilisant la stratégie BFS.
        """
        # Vérifier la fin de la punition
        self.check_punishment()
        if self.is_punished:
            return

        # Respecter le délai avant de bouger
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0

        # Vérifier si l'agent est invisible
        self.check_invisibility()

        # Priorité : Aller chercher une potion si aucune n'est active
        if not self.is_invisible:
            nearest_potion = self.find_nearest_potion(environment)
            if nearest_potion:
                path = self.bfs((self.x, self.y), nearest_potion, environment)
                if path:
                    self.path_stack = deque(path[1:])
                if self.path_stack:
                    self.x, self.y = self.path_stack.popleft()
                    self.handle_potion_interactions(environment)
                    return

        # Si l'agent a un bonbon, retour à la position initiale
        if self.has_candy:
            path = self.bfs((self.x, self.y), self.initial_position, environment)
            if path:
                self.path_stack = deque(path[1:])
            if self.path_stack:
                self.x, self.y = self.path_stack.popleft()
            if (self.x, self.y) == self.initial_position:
                self.has_candy = False
                self.score += 1
                print(f"{type(self).__name__} scored! Current score: {self.score}")
            return

        # Sinon, chercher un bonbon
        target_x, target_y = self.set_target(environment)
        path = self.bfs((self.x, self.y), (target_x, target_y), environment)
        if path:
            self.path_stack = deque(path[1:])
        if self.path_stack:
            self.x, self.y = self.path_stack.popleft()

        # Gérer les interactions avec les bonbons
        self.handle_candy_interactions(environment)
