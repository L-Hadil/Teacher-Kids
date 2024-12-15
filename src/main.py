from src.game import Game

if __name__ == "__main__":
    GRID_WIDTH = 20
    GRID_HEIGHT = 15
    CELL_SIZE = 40

    GAME_DURATION = 60  # Temps limite en secondes (2 minutes)

    COLORING_ZONE = (2, 1, 4, 3)  # Zone de coloriage
    CANDY_ZONE = (17, 12, 19, 14)  # Zone des bonbons
    CANDY_COUNT = 10  # Nombre de bonbons affichés

    CANDY_ICON_PATH = "../assets/candy.png"
    TEACHER_ICON_PATH = "../assets/teacher.png"
    CHILD1_ICON_PATH = "../assets/DirectToCandy.png"
    CHILD2_ICON_PATH = "../assets/LongestPath.png"
    CHILD3_ICON_PATH = "../assets/WaitAndGo.png"
    CHILD4_ICON_PATH = "../assets/DistractorKid.png"
    POTION_ICON_PATH = "../assets/potion.png"

    game = Game(
        GRID_WIDTH,
        GRID_HEIGHT,
        CELL_SIZE,
        CANDY_ZONE,
        COLORING_ZONE,
        CANDY_COUNT,
        CANDY_ICON_PATH,
        TEACHER_ICON_PATH,
        CHILD1_ICON_PATH,
        CHILD2_ICON_PATH,
        CHILD3_ICON_PATH,
        CHILD4_ICON_PATH,
        potion_icon_path=POTION_ICON_PATH,
        game_duration=GAME_DURATION

    )
    game.run()
