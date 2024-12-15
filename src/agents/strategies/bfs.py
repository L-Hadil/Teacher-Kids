from collections import deque
from src.agents.kid import Kid

class bfs(Kid):
    def __init__(self, x, y, cell_size, icon_path):
        super().__init__(x, y, cell_size, icon_path)
        self.path_stack = deque()  # Initialize an empty deque for BFS
        self.initial_position = (x, y)  # Store the initial position

    def bfs(self, start, target, environment):
        """
        Perform BFS to find the shortest path to the target.

        Args:
        - start (tuple): Starting position (x, y)
        - target (tuple): Target position (x, y)
        - environment (Environment): Game environment

        Returns:
        - path (list): Shortest path from start to target as a list of (x, y) tuples
        """
        queue = deque([(start, [start])])  # Initialize BFS queue
        visited = set()  # Keep track of visited positions

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == target:
                return path

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # Explore neighbors
                nx, ny = x + dx, y + dy
                if (0 <= nx < environment.width and 0 <= ny < environment.height and
                        (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

        return []  # Return empty list if no path is found

    def move(self, environment, teacher_position):
        """
        Move the agent using BFS.
        """
        # Respect the movement delay
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0

        # Determine the current target
        if self.has_candy:
            target_x, target_y = self.initial_position  # Return to initial position
        else:
            target_x, target_y = self.set_target(environment)  # Move towards candy or coloring zone

        # Perform BFS to find the shortest path
        path = self.bfs((self.x, self.y), (target_x, target_y), environment)
        if path:
            self.path_stack = deque(path[1:])  # Store the path (excluding the starting position)

        # Move to the next position in the path
        if self.path_stack:
            self.x, self.y = self.path_stack.popleft()

            # Check if the agent has returned to its initial position
            if (self.x, self.y) == self.initial_position and self.has_candy:
                self.has_candy = False
                self.score += 1

        # Handle candy interactions
        self.handle_candy_interactions(environment)