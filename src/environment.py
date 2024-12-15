import pygame
class Environment:
    def __init__(self, width, height, cell_size, candy_zone, coloring_zone, candy_count, candy_icon_path):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.candy_zone = candy_zone
        self.coloring_zone = coloring_zone
        self.candy_count = candy_count
        self.candy_icon = pygame.image.load(candy_icon_path)  # Load the candy icon
        self.candy_icon = pygame.transform.scale(self.candy_icon, (cell_size, cell_size))  # Resize to cell size
        self.agents_positions = []  # List to track agents' positions
        self.kids_doing_homework = 0  # Counter for kids doing homework

    def is_in_candy_zone(self, x, y):
        """Check if a given (x, y) position is within the candy zone."""
        return (self.candy_zone[0] <= x <= self.candy_zone[2] and
                self.candy_zone[1] <= y <= self.candy_zone[3])

    def add_agent_to_coloring_zone(self, x, y):
        if self.is_in_coloring_zone(x, y) and (x, y) not in self.agents_positions:
            self.agents_positions.append((x, y))
            return True
        return False

    def remove_agent_from_coloring_zone(self, x, y):
        if (x, y) in self.agents_positions:
            self.agents_positions.remove((x, y))
            return True
        return False

    def update_kids_status(self, kids):
        # Reset homework counter
        self.kids_doing_homework = 0  # Reset homework count each time before updating

        # Count how many kids are doing homework
        for kid in kids:
            if kid.do_homework:
                self.kids_doing_homework += 1

    def draw(self, screen):
        # Draw the grid
        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (211, 211, 211), rect)  # Light gray for neutral space
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Black borders

        # Draw the coloring zone
        for x in range(self.coloring_zone[0], self.coloring_zone[2] + 1):
            for y in range(self.coloring_zone[1], self.coloring_zone[3] + 1):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (144, 238, 144), rect)  # Light green for the coloring zone
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Black borders

        # Draw the candy zone
        for x in range(self.candy_zone[0], self.candy_zone[2] + 1):
            for y in range(self.candy_zone[1], self.candy_zone[3] + 1):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 239, 213), rect)  # Beige for the candy zone
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Black borders

        # Display candies
        count = 0
        for x in range(self.candy_zone[0], self.candy_zone[2] + 1):
            for y in range(self.candy_zone[1], self.candy_zone[3] + 1):
                if count < self.candy_count:
                    if self.is_in_candy_zone(x, y):  # Check if candy is within the candy zone
                        screen.blit(self.candy_icon, (x * self.cell_size, y * self.cell_size))
                    count += 1
