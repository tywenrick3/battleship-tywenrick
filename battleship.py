# Author: <Ty Wenrick>
# Assignment #6 - Battleship
# Date due: 2021-05-06
# I pledge that I have completed this assignment without
# collaborating with anyone else, in conformance with the
# NYU School of Engineering Policies and Procedures on
# Academic Misconduct.

import random

### DO NOT EDIT BELOW (with the exception of MAX_MISSES) ###

HIT_CHAR = 'x'
MISS_CHAR = 'o'
BLANK_CHAR = '.'
HORIZONTAL = 'h'
VERTICAL = 'v'
MAX_MISSES = 20
SHIP_SIZES = {
    "carrier": 5,
    "battleship": 4,
    "cruiser": 3,
    "submarine": 3,
    "destroyer": 2
}
NUM_ROWS = 10
NUM_COLS = 10
ROW_IDX = 0
COL_IDX = 1
MIN_ROW_LABEL = 'A'
MAX_ROW_LABEL = 'J'


def get_random_position():
    """Generates a random location on a board of NUM_ROWS x NUM_COLS."""

    row_choice = chr(
        random.choice(
            range(
                ord(MIN_ROW_LABEL),
                ord(MIN_ROW_LABEL) + NUM_ROWS
            )
        )
    )

    col_choice = random.randint(0, NUM_COLS - 1)

    return (row_choice, col_choice)


def play_battleship():
    """Controls flow of Battleship games including display of
    welcome and goodbye messages.

    :return: None
    """

    print("Let's Play Battleship!\n")

    game_over = False

    while not game_over:

        game = Game()
        game.display_board()

        while not game.is_complete():
            pos = game.get_guess()
            result = game.check_guess(pos)
            game.update_game(result, pos)
            game.display_board()

        game_over = end_program()

    print("Goodbye.")


### DO NOT EDIT ABOVE (with the exception of MAX_MISSES) ###

# get a key from a dict with a value
def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key

    return "key doesn't exist"


class Ship:

    def __init__(self, name, start_position, orientation, sunk=False):
        """Creates a new ship with the given name, placed at start_position in the
        provided orientation. The number of positions occupied by the ship is determined
        by looking up the name in the SHIP_SIZE dictionary.

        :param name: the name of the ship
        :param start_position: tuple representing the starting position of ship on the board
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return: None
        """
        self.size = SHIP_SIZES[name]
        self.name = name
        self.start_position = start_position
        self.sunk = False
        self.orientation = orientation
        self.positions = {start_position: False}
        row = self.start_position[0]
        col = self.start_position[1]

        if self.orientation == VERTICAL:
            for i in range(self.size):
                self.positions[((chr(ord(row) + i)), col)] = False
        if self.orientation == HORIZONTAL:
            for i in range(self.size):
                self.positions[row, col + i] = False


class Game:

    def __init__(self, max_misses=MAX_MISSES):
        """ Creates a new game with max_misses possible missed guesses.
        The board is initialized in this function and ships are randomly
        placed on the board.

        :param max_misses: maximum number of misses allowed before game ends
        """
        self.max_misses = max_misses
        self.guesses = []
        self.ships = []
        self.initialize_board()
        self.create_and_place_ships()

    def initialize_board(self):
        """Sets the board to it's initial state with each position occupied by
        a period ('.') string.

        :return: None
        """
        self.board = {}
        for i in range(10):
            self.board[chr(ord(MIN_ROW_LABEL) + i)] = [".", ".", ".", ".", ".", ".", ".", ".", ".", "."]

    def in_bounds(self, start_position, ship_size, orientation):
        """Checks that a ship requiring ship_size positions can be placed at start position.

        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return status: True if ship placement inside board boundary, False otherwise
        """
        row = start_position[0]
        col = start_position[1]
        if orientation == HORIZONTAL:
            for i in range(ship_size):
                if col > 9:
                    return False
                col += 1
        if orientation == VERTICAL:
            for i in range(ship_size):
                pos = ord(row)
                if pos > ord(MAX_ROW_LABEL):
                    return False
                row = chr(ord(row)+1)
        return True

    def overlaps_ship(self, start_position, ship_size, orientation):
        """Checks for overlap between previously placed ships and a potential new ship
        placement requiring ship_size positions beginning at start_position in the
        given orientation.

        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :param orientation: the orientation of the ship ('v' - vertical, 'h' - horizontal)
        :return status: True if ship placement overlaps previously placed ship, False otherwise
        """

        #ship = self.ships[len(self.ships) - 1]
        #positions = ship.positions

        for i in range(len(self.ships)):
            ship = self.ships[i]
            positions = ship.positions
            row = start_position[0]
            col = start_position[1]
            current_position = start_position

            if orientation == HORIZONTAL:
                for j in range(ship_size):
                    if current_position in positions:
                        return True
                    col += 1
                    current_position = (row, col)
            if orientation == VERTICAL:
                for j in range(ship_size):
                    if current_position in positions:
                        return True
                    row = chr(ord(row)+1)
                    current_position = (row, col)

        return False

    def place_ship(self, start_position, ship_size):
        """Determines if placement is possible for ship requiring ship_size positions placed at
        start_position. Returns the orientation where placement is possible or None if no placement
        in either orientation is possible.

        :param start_position: tuple representing the starting position of ship on the board
        :param ship_size: number of positions needed to place ship
        :return orientation: 'h' if horizontal placement possible, 'v' if vertical placement possible,
            None if no placement possible
        """

        if self.in_bounds(start_position, ship_size, HORIZONTAL) and not self.overlaps_ship(start_position, ship_size, HORIZONTAL):
            return HORIZONTAL
        elif self.in_bounds(start_position, ship_size, VERTICAL) and not self.overlaps_ship(start_position, ship_size, VERTICAL):
            return VERTICAL
        else:
            return None

    def create_and_place_ships(self):
        """Instantiates ship objects with valid board placements.

        :return: None
        """
        for i in range(len(self._ship_types)):
            valid = False
            while not valid:
                start_position = get_random_position()
                size = SHIP_SIZES[self._ship_types[i]]
                if self.place_ship(start_position, size) == HORIZONTAL:
                    self.ships.append(Ship(self._ship_types[i], start_position, HORIZONTAL))
                    valid = True
                elif self.place_ship(start_position, size) == VERTICAL:
                    self.ships.append(Ship(self._ship_types[i], start_position, VERTICAL))
                    valid = True


    ########## DO NOT EDIT #########

    _ship_types = ["carrier", "battleship", "cruiser", "submarine", "destroyer"]

    def display_board(self):
        """ Displays the current state of the board."""

        print()
        print("  " + ' '.join('{}'.format(i) for i in range(len(self.board))))
        for row_label in self.board.keys():
            print('{} '.format(row_label) + ' '.join(self.board[row_label]))
        print()

    ########## DO NOT EDIT #########


def end_program():
    """Prompts the user with "Play again (Y/N)?" The question is repeated
    until the user enters a valid response (Y/y/N/n). The function returns
    False if the user enters 'Y' or 'y' and returns True if the user enters
    'N' or 'n'.

    :return response: boolean indicating whether to end the program
    """
    while True:
        play_again = input("Play again (Y/N)? ")
        if play_again == 'Y' or play_again == 'y':
            return False
        if play_again == 'N' or play_again == 'n':
            return True


def main():
    """Executes one or more games of Battleship."""

    # play_battleship()
    game = Game()
    game.display_board()

    print(game.create_and_place_ships())


if __name__ == "__main__":
    main()
