from game import GoldRush


def play_game():
    print("Welcome to Gold Rush!")
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))

    game = GoldRush(rows, cols)
    game.load_board()
    game.print_matrix()

    while not game.winner:
        for player in [game.PLAYER1, game.PLAYER2]:
            direction = input(f"{player}, enter your move(up, down, left, right): ").strip().lower()
            game.move_player(player, direction)
            game.print_matrix()
            if game._check_win(player):
                print(f"{player} wins!")
                return

if __name__ == "__main__":
    play_game()



