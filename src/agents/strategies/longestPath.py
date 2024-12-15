from src.agents.kid import Kid
from venv import logger
from collections import deque
class LongestPath(Kid):
    def __init__(self, x, y, cell_size, icon_path, candy_zone):
        super().__init__(x, y, cell_size, icon_path)
        self.initial_position = (x, y)  # Store the initial position
        self.path_stack = []  # Track the path the agent takes
        self.candy_zone = candy_zone  # The cell where candy is located
        self.found_candy = False  # Flag to check if the agent has reached the candy

    def manhattan_distance(self, point1, point2):
        """
        Calculate Manhattan distance between two points.
        """
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def move_to_candy(self, target_x, target_y):
        """
        Move the agent directly to the candy location (if it's within range).
        """
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

    def move(self, environment, teacher_position):
        """
        Move the agent first to the candy zone, and then return to the initial position.
        """
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0  # Reset the tick counter

        # If the agent has found the candy and is ready to return to its starting position
        if self.found_candy and self.path_stack:
            self.x, self.y = self.path_stack.pop()  # Go back via the path stack
            if not self.path_stack:  # If back at the initial position
                self.found_candy = False
                self.has_candy = False
                self.score += 1  # Reward for returning to the start position
            return

        # If not carrying candy, check if we're close enough to the candy zone
        if not self.found_candy and self.manhattan_distance((self.x, self.y), self.candy_zone) == 0:
            self.move_to_candy(self.candy_zone[0], self.candy_zone[1])  # Move directly to the candy
            self.found_candy = True
            self.has_candy = True  # Candy collected
            self.score += 1
            self.handle_candy_interactions(environment)
            return

        # If not yet near the candy zone, move along the grid's borders
        closest_border = self.find_closest_border((self.x, self.y), environment)
        next_x, next_y = self.move_to_border((self.x, self.y), closest_border, environment)
        self.x, self.y = next_x, next_y

    def find_closest_border(self, position, environment):
        """
        Find the closest border to the current position (top, bottom, left, right).
        """
        x, y = position
        distances = {
            'top': y,  # Distance to top row (y=0)
            'bottom': environment.height - y - 1,  # Distance to bottom row (y=height-1)
            'left': x,  # Distance to left column (x=0)
            'right': environment.width - x - 1  # Distance to right column (x=width-1)
        }

        # Find the border with the minimum distance
        closest_border = min(distances, key=distances.get)
        return closest_border

    def move_to_border(self, position, closest_border, environment):
        """
        Move the agent step by step along the closest border towards the target.
        """
        x, y = position
        target_x, target_y = self.set_target(environment)

        # Move along the closest border
        if closest_border == 'top':
            if x < target_x:  # Move to the right along the top row
                next_x, next_y = x + 1, 0
            else:  # Move to the left along the top row
                next_x, next_y = x - 1, 0
        elif closest_border == 'bottom':
            if x < target_x:  # Move to the right along the bottom row
                next_x, next_y = x + 1, environment.height - 1
            else:  # Move to the left along the bottom row
                next_x, next_y = x - 1, environment.height - 1
        elif closest_border == 'left':
            if y < target_y:  # Move down the left column
                next_x, next_y = 0, y + 1
            else:  # Move up the left column
                next_x, next_y = 0, y - 1
        elif closest_border == 'right':
            if y < target_y:  # Move down the right column
                next_x, next_y = environment.width - 1, y + 1
            else:  # Move up the right column
                next_x, next_y = environment.width - 1, y - 1

        return next_x, next_y
