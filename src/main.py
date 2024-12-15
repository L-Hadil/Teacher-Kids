from src.game import Game

if __name__ == "__main__":
    GRID_WIDTH = 20
    GRID_HEIGHT = 15
    CELL_SIZE = 40
    GAME_DURATION = 120  # Temps limite en secondes (2 minutes)
    COLORING_ZONE = (2, 1, 4, 3)  # Zone de coloriage
    CANDY_ZONE = (17, 12, 19, 14)  # Zone des bonbons

    CANDY_ICON_PATH = "../assets/candy.png"
    TEACHER_ICON_PATH = "../assets/teacher.png"
    CHILD1_ICON_PATH = "../assets/DirectToCandy.png"
    CHILD2_ICON_PATH = "../assets/LongestPath.png"
    CHILD3_ICON_PATH = "../assets/WaitAndGo.png"
    CHILD4_ICON_PATH = "../assets/DistractorKid.png"
    CHILD5_ICON_PATH = "../assets/bfs.png"

    # Demander le nombre de bonbons à l'utilisateur
    while True:
        try:
            CANDY_COUNT = int(input("Veuillez entrer le nombre de bonbons (entre 1 et 50) : "))
            if 1 <= CANDY_COUNT <= 50:
                break
            else:
                print("Veuillez entrer un nombre compris entre 1 et 50.")
        except ValueError:
            print("Erreur : Veuillez entrer un nombre entier.")

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
        CHILD5_ICON_PATH,
        game_duration=GAME_DURATION
    )
    game.run()