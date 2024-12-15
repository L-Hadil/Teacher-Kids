from collections import deque
from src.agents.child import Child

class BFSAgent(Child):
    def __init__(self, x, y, cell_size, icon_path):
        super().__init__(x, y, cell_size, icon_path)
        self.movement_queue = deque()  # Déque pour le BFS
        self.start_position = (x, y)  # Position de départ enregistrée

    def find_shortest_path(self, start, goal, environment):
        """
        Réalise une recherche BFS pour trouver le chemin le plus court vers la cible.

        Args:
        - start (tuple): Position de départ (x, y)
        - goal (tuple): Position cible (x, y)
        - environment (Environment): Environnement du jeu

        Returns:
        - chemin (list): Chemin le plus court sous forme de liste de tuples (x, y)
        """
        queue = deque([(start, [start])])  # Initialisation de la file pour le BFS
        visited_nodes = set()  # Positions déjà visitées

        while queue:
            (current_x, current_y), path = queue.popleft()
            if (current_x, current_y) == goal:
                return path

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # Exploration des voisins
                neighbor_x, neighbor_y = current_x + dx, current_y + dy
                if (0 <= neighbor_x < environment.width and
                        0 <= neighbor_y < environment.height and
                        (neighbor_x, neighbor_y) not in visited_nodes):
                    visited_nodes.add((neighbor_x, neighbor_y))
                    queue.append(((neighbor_x, neighbor_y), path + [(neighbor_x, neighbor_y)]))

        return []  # Retourne une liste vide si aucun chemin n'est trouvé

    def perform_move(self, environment, supervisor_position):
        """
        Effectue un déplacement en utilisant le BFS.
        """
        # Gestion du délai de déplacement
        self.action_count += 1
        if self.action_count < Child.DEFAULT_ACTION_DELAY:
            return
        self.action_count = 0

        # Détermine la cible actuelle
        if self.is_holding_item:
            target_x, target_y = self.start_position  # Retour à la position initiale
        else:
            target_x, target_y = self.find_target(environment)  # Recherche de l'objectif (bonbon, zone colorée)

        # Recherche du chemin le plus court avec BFS
        shortest_path = self.find_shortest_path((self.x, self.y), (target_x, target_y), environment)
        if shortest_path:
            self.movement_queue = deque(shortest_path[1:])  # Enregistre le chemin sauf la position actuelle

        # Déplacement vers la prochaine position
        if self.movement_queue:
            self.x, self.y = self.movement_queue.popleft()

            # Vérifie si l'agent est retourné à sa position initiale
            if (self.x, self.y) == self.start_position and self.is_holding_item:
                self.is_holding_item = False
                self.points += 1

        # Gestion des interactions avec les bonbons
        self.process_item_interactions(environment)
