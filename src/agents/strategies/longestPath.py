from collections import deque
import heapq  # For priority queue (min-heap)

from src.agents.kid import Kid


class LongestPath(Kid):
    def __init__(self, x, y, cell_size, icon_path):
        super().__init__(x, y, cell_size, icon_path)
        self.path_stack = deque()  # Initialize an empty deque for the path
        self.initial_position = (x, y)  # Store the initial position

    def is_border(self, x, y, environment):
        """Check if the position (x, y) is next to the border of the grid."""
        return x == 0 or x == environment.width - 1 or y == 0 or y == environment.height - 1

    def dijkstra(self, start, target, environment, teacher_position):
        """
        Perform Dijkstra's algorithm to find the shortest path from start to target.
        The path should avoid the teacher's position and aim for the borders.
        """
        # Priority queue for exploring the least costly paths first
        pq = [(0, start, [start])]  # (cost, (x, y), path)
        visited = set()  # Set of visited positions
        distance_map = {start: 0}  # Map of minimum cost to reach each position

        while pq:
            cost, (x, y), path = heapq.heappop(pq)  # Get the position with the least cost

            # If we have reached the target, return the path
            if (x, y) == target:
                return path

            # Explore neighbors (up, down, left, right)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy

                # Ensure the new position is within bounds and hasn't been visited
                if (0 <= nx < environment.width and 0 <= ny < environment.height and
                        (nx, ny) not in visited and (nx, ny) != teacher_position):
                    # Favor positions near borders (even if not exactly on borders)
                    if self.is_border(nx, ny, environment):
                        new_cost = cost + 1
                    else:
                        new_cost = cost + 2  # Slightly higher cost to move away from the border

                    # Only explore this new position if it's cheaper to reach it
                    if (nx, ny) not in distance_map or new_cost < distance_map[(nx, ny)]:
                        distance_map[(nx, ny)] = new_cost
                        heapq.heappush(pq, (new_cost, (nx, ny), path + [(nx, ny)]))

        return []  # Return empty list if no path is found

    def manhattan_distance(self, x1, y1, x2, y2):
        """Calculate the Manhattan distance between two points."""
        return abs(x1 - x2) + abs(y1 - y2)

    def move(self, environment, teacher_position):
        """
        Move the agent using Dijkstra's algorithm first, then fall back to Manhattan distance if no path is found.
        The agent prefers to stay next to the borders, avoiding the teacher.
        """
        # Respect the movement delay
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0

        # Determine the current target
        if self.has_candy:
            target_x, target_y = self.initial_position  # Return to initial position after collecting candy
        else:
            target_x, target_y = self.set_target(environment)  # Move towards candy or coloring zone

        # Use Dijkstra's algorithm to find the shortest path to the target
        path = self.dijkstra((self.x, self.y), (target_x, target_y), environment, teacher_position)

        if path:
            # If Dijkstra found a path, store it in the path_stack (excluding the starting position)
            self.path_stack = deque(path[1:])
        else:
            # If Dijkstra failed, fall back to Manhattan distance-based movement
            # Move directly towards the target using Manhattan distance
            if self.x < target_x:
                self.x += 1
            elif self.x > target_x:
                self.x -= 1

            if self.y < target_y:
                self.y += 1
            elif self.y > target_y:
                self.y -= 1

        # Step 4: Move to the next position in the path (if any)
        if self.path_stack:
            self.x, self.y = self.path_stack.popleft()

            # Check if the agent has returned to its initial position after collecting candy
            if (self.x, self.y) == self.initial_position and self.has_candy:
                self.has_candy = False
                self.score += 1

        # Handle candy interactions (if applicable)
        self.handle_candy_interactions(environment)
