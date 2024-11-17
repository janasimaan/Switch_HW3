from Matrix import Matrix
import random

class Directions:
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @staticmethod
    def get(direction):
        try:
            return getattr(Directions, direction.upper())
        except AttributeError:
            raise ValueError(f"Invalid direction: {direction}")


class GoldRush(Matrix):
    WALL = "🧱"
    COIN = "💰"
    EMPTY = "⬜"
    PLAYER1 = "🤠"
    PLAYER2 = "👩‍🚀"

    def __init__(self, rows, cols):
        super().__init__(rows, cols)
        self.player1_score = 0
        self.player2_score = 0
        self.winner = None
        self.coins = 0

    def load_board(self):
        while True:
            self.matrix = []
            self.coins = 0
            self.place_walls_and_coins()
            self.matrix[0][0] = self.PLAYER1
            self.matrix[self.rows - 1][self.cols - 1] = self.PLAYER2
            if self.coins >= 10:
                break

    def place_walls_and_coins(self):
        elements = [self.COIN, self.EMPTY, self.WALL]
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                if c % 2 == 0:  # Only consider even columns
                    if random.choice([True, False]):  # Randomly decide whether to place a wall
                        row.append(self.WALL)
                    else:
                        row.append(self.EMPTY)  # Or something else (coin, etc.)
                else:
                    row.append(self.EMPTY)  # Non-even columns, fill with empty space
            self.matrix.append(row)
        self._scatter_coins()


    def _scatter_coins(self):
        elements = [self.COIN, self.EMPTY]
        for r in range(self.rows):
            if r % 2 != 0:
                for c in range(1, self.cols, random.randint(1, 3)):
                    element = random.choice(elements)
                    self.matrix[r][c] = element
                    if element == self.COIN:
                        self.coins += 1

    def move_player(self, player, direction):
        current_row, current_col = self._find_player(player)
        self._move(current_row, current_col, player, direction)

    def _find_player(self, player):
        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                if value == player:
                    return i, j
        raise ValueError(f"{player} not found on the board!")

    def _move(self, current_row, current_col, player, direction):
        other_player = self._get_opponent(player)
        try:
            delta_row, delta_col = Directions.get(direction)
        except ValueError as e:
            print(e)
            return
        new_row, new_col = current_row + delta_row, current_col + delta_col
        if self._is_valid_move(new_row, new_col, other_player):
            if self.matrix[new_row][new_col] == self.COIN:
                self._score(player)
                total_score = self.player1_score if player == self.PLAYER1 else self.player2_score
                print(f"{player} collected a coin! 🎉 Total score: {total_score}")
            self._update_position(current_row, current_col, new_row, new_col, player)
        return self._check_win(player)

    def _update_position(self, current_row, current_col, new_row, new_col, player):
        self.matrix[current_row][current_col] = self.EMPTY
        self.matrix[new_row][new_col] = player

    def _get_opponent(self, player):
        return self.PLAYER2 if player == self.PLAYER1 else self.PLAYER1

    def _is_valid_move(self, row, col, opponent):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.matrix[row][col] not in [self.WALL, opponent]

    def _score(self, player):
        if player == self.PLAYER1:
            self.player1_score += 10
        elif player == self.PLAYER2:
            self.player2_score += 10

    def _check_win(self, player):
        if player == self.PLAYER1 and self.player1_score >= 100:
            self.winner = self.PLAYER1
        elif player == self.PLAYER2 and self.player2_score >= 100:
            self.winner = self.PLAYER2
        return self.winner is not None
