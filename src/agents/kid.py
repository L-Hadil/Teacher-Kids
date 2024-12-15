import pygame
from abc import ABC, abstractmethod
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Kid(ABC):
    DEFAULT_TICK_DELAY = 5  # Default speed for all kids

    def __init__(self, x, y, cell_size, icon_path):
        self.x = x
        self.y = y
        self.initial_position = (x, y)
        self.path_stack = []
        self.cell_size = cell_size
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (cell_size, cell_size))
        self.has_candy = False
        self.score = 0
        self.tick_count = 0
        self.do_homework = False  # Flag to track homework status
        self.homework_time = 0  # Timer for homework duration (in ticks)
        self.frozen_until = 0  # Tracks the moment when the kid will be unfrozen
        self.carrying_candy = False

    def move(self, environment, teacher_position):
        if self.do_homework:
            # If the kid is doing homework, stop their movement
            self.homework_time += 1
            if self.homework_time >= 750:  # 25 seconds at 30 FPS = 750 ticks
                self.do_homework = False
                self.homework_time = 0
                logger.info(f"{type(self).__name__} has completed their homework!")
            return  # Kid is frozen, they can't move

        # Normal movement behavior
        self.tick_count += 1
        if self.tick_count < Kid.DEFAULT_TICK_DELAY:
            return

        self.tick_count = 0
        # Movement logic: move towards the next position in the path stack
        if self.path_stack:
            next_pos = self.path_stack.pop()
            self.x, self.y = next_pos
        else:
            self.x += 1  # Default behavior: moving right



    def set_target(self, environment):
        """Determine the current target for the kid."""
        if self.has_candy:
            if self.path_stack:
                return self.path_stack[-1]
            else:
                logger.warning(f"{type(self).__name__} path_stack is empty. Returning to initial position.")
                return self.initial_position
        else:
            target_x = (environment.candy_zone[0] + environment.candy_zone[2]) // 2
            target_y = (environment.candy_zone[1] + environment.candy_zone[3]) // 2
            return target_x, target_y

    def handle_candy_interactions(self, environment):
        """Handle interactions between the kid and the candy zone."""
        if self.has_candy and self.path_stack and (self.x, self.y) == self.path_stack[-1]:
            self.path_stack.pop()
            if not self.path_stack:
                self.has_candy = False
                self.score += 1
                logger.info(f"{type(self).__name__} delivered candy! Score: {self.score}")
        elif not self.has_candy and (self.x, self.y) == self.set_target(environment):
            if environment.candy_count > 0:
                self.has_candy = True
                environment.candy_count -= 1
                logger.info(f"{type(self).__name__} picked a candy! Remaining candies: {environment.candy_count}")

    def draw(self, screen):
        """Draw the kid on the screen, indicating homework if active."""
        if self.do_homework:
            # Draw with a red box to indicate homework
            homework_rect = pygame.Rect(self.x * self.cell_size, self.y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, (255, 0, 0), homework_rect)  # Red
            font = pygame.font.Font(None, 24)
            text = font.render("Devoirs", True, (255, 255, 255))  # White text
            screen.blit(text, (self.x * self.cell_size + 10, self.y * self.cell_size + 10))
        else:
            # Normal drawing of the kid
            screen.blit(self.icon, (self.x * self.cell_size, self.y * self.cell_size))
