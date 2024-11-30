from game import Game

if __name__ == "__main__":

    GRID_WIDTH = 20
    GRID_HEIGHT = 15
    CELL_SIZE = 40

    # Nouvelle position des zones
    COLORING_ZONE = (2, 1, 4, 3)  # Zone verte au centre approximatif
    CANDY_ZONE = (17, 12, 19, 14)  # Zone beige à droite en bas
    CANDY_COUNT = 7  # Nombre de bonbons affichés

    CANDY_ICON_PATH = "../assets/candy.png"


    game = Game(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, CANDY_ZONE, COLORING_ZONE, CANDY_COUNT, CANDY_ICON_PATH)
    game.run()
