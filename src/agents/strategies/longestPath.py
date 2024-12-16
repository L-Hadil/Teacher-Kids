from collections import deque
import heapq
from src.agents.kid import Kid


class LongestPath(Kid):
    def __init__(self, x, y, cell_size, icon_path):
        super().__init__(x, y, cell_size, icon_path)
        self.path_stack = deque()  # Initialise une deque pour le chemin
        self.initial_position = (x, y)  # Position initiale de l'agent

    def is_border(self, x, y, environment):
        """Vérifie si la position (x, y) est proche de la bordure de la grille."""
        return x == 0 or x == environment.width - 1 or y == 0 or y == environment.height - 1

    def dijkstra(self, start, target, environment, teacher_position):
        """
        Implémente l'algorithme de Dijkstra pour trouver le chemin le plus court vers la cible.
        """
        pq = [(0, start, [start])]  # (coût, (x, y), chemin)
        visited = set()
        distance_map = {start: 0}

        while pq:
            cost, (x, y), path = heapq.heappop(pq)

            if (x, y) == target:
                return path

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy

                if (0 <= nx < environment.width and 0 <= ny < environment.height and
                        (nx, ny) not in visited and (nx, ny) != teacher_position):
                    if self.is_border(nx, ny, environment):
                        new_cost = cost + 1
                    else:
                        new_cost = cost + 2

                    if (nx, ny) not in distance_map or new_cost < distance_map[(nx, ny)]:
                        distance_map[(nx, ny)] = new_cost
                        heapq.heappush(pq, (new_cost, (nx, ny), path + [(nx, ny)]))

        return []  # Aucun chemin trouvé

    def move(self, environment, teacher_position):
        """
        Déplace l'agent en utilisant Dijkstra, puis Manhattan si aucun chemin trouvé.
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

        # Vérifier la fin de l'invisibilité
        self.check_invisibility()

        # Prioriser les potions si disponibles
        if not self.is_invisible:
            nearest_potion = self.find_nearest_potion(environment)
            if nearest_potion:
                path = self.dijkstra((self.x, self.y), nearest_potion, environment, teacher_position)
                if path:
                    self.path_stack = deque(path[1:])
                if self.path_stack:
                    self.x, self.y = self.path_stack.popleft()
                    self.handle_potion_interactions(environment)
                    return

        # Retourner à la base si un bonbon est collecté
        if self.has_candy:
            path = self.dijkstra((self.x, self.y), self.initial_position, environment, teacher_position)
            if path:
                self.path_stack = deque(path[1:])
            if self.path_stack:
                self.x, self.y = self.path_stack.popleft()
            if (self.x, self.y) == self.initial_position:
                self.has_candy = False
                self.score += 1
                print(f"{type(self).__name__} scored! Current score: {self.score}")
            return

        # Se déplacer vers un bonbon
        target_x, target_y = self.set_target(environment)
        path = self.dijkstra((self.x, self.y), (target_x, target_y), environment, teacher_position)
        if path:
            self.path_stack = deque(path[1:])
        if self.path_stack:
            self.x, self.y = self.path_stack.popleft()

        # Gérer les interactions avec les bonbons
        self.handle_candy_interactions(environment)
