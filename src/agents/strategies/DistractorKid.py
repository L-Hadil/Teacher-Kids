import math
from src.agents.kid import Kid
from venv import logger
class DistractorKid(Kid):
    DISTRACTION_RADIUS = 5
    FAR_DISTANCE_THRESHOLD = 8

    def __init__(self, x, y, cell_size, icon_path):
        super().__init__(x, y, cell_size, icon_path)
        self.initial_position = (x, y)
        self.distracting = True
        self.current_target = None
        self.path_taken = []  # Store the path taken by the agent

    def move(self, environment, teacher_position):
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return
        self.tick_count = 0

        # If the agent has a candy, return to its initial position, retracing its steps
        if self.has_candy:
            self.return_to_coloring_zone(environment, teacher_position)
            return

        # Determine the distance to the teacher
        distance_to_teacher = math.sqrt(
            (self.x - teacher_position[0]) ** 2 + (self.y - teacher_position[1]) ** 2
        )

        # Define the mode (distraction or candy collection)
        if distance_to_teacher <= self.DISTRACTION_RADIUS:
            self.distracting = True
        elif distance_to_teacher > self.FAR_DISTANCE_THRESHOLD:
            self.distracting = False

        # Behavior based on the mode
        if self.distracting:
            self.current_target = self.calculate_distracting_position(environment, teacher_position)
        else:
            self.current_target = self.find_candy(environment)

        # Move towards the target
        if self.current_target:
            self.path_taken.append((self.x, self.y))  # Store the current position in the path
            self.move_towards_target(*self.current_target)

        # Handle candy interactions
        self.handle_candy_interactions(environment)

    def return_to_coloring_zone(self, environment, teacher_position):
        """
        Returns to the initial position while maximizing the distance from the teacher.
        Uses the path taken initially to retrace steps.
        """
        if self.path_taken:  # If there's a recorded path, retrace it
            next_position = self.path_taken.pop()
            self.x, self.y = next_position
            logger.info(f"Returning to coloring zone at {next_position}.")
        else:
            # If no path has been stored (e.g., if the agent hasn't moved yet), return directly to initial position
            self.x, self.y = self.initial_position
            logger.info(f"Returning to initial position {self.initial_position}.")

        # Once back at the initial position, drop the candy and score
        if (self.x, self.y) == self.initial_position:
            self.has_candy = False
            self.score += 1
            logger.info(f"DistractorKid scored! Current score: {self.score}")
            self.distracting = True  # Resuming distraction after scoring a point

    def find_candy(self, environment):
        """
        Finds the position of an available candy in the candy zone.
        """
        for x in range(environment.candy_zone[0], environment.candy_zone[2] + 1):
            for y in range(environment.candy_zone[1], environment.candy_zone[3] + 1):
                if environment.candy_zone:
                    return (x, y)
        return None

    def calculate_distracting_position(self, environment, teacher_position):
        """
        Calculates a position near the teacher to distract them.
        """
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in offsets:
            new_x = teacher_position[0] + dx
            new_y = teacher_position[1] + dy
            if 0 <= new_x < environment.width and 0 <= new_y < environment.height:
                return (new_x, new_y)
        return teacher_position

    def move_towards_target(self, target_x, target_y):
        """
        Moves the agent towards the given target.
        """
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1
