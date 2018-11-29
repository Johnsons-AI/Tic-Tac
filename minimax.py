#!/usr/bin/env python3
from math import inf as infinity
from copy import deepcopy
import random
import platform
import time
import csv
from os import system

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


class Player_Ai:
    def __init__(self, name, optimal_percent, optimal_moves=0, total_moves=0):
        self.name = name.capitalize()
        self.optimal_percent = optimal_percent
        self.optimal_moves = optimal_moves
        self.total_moves = total_moves


def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    This function tests if a specific player wins. Possibilities:
    * Three rows    [X X X] or [O O O]
    * Three cols    [X X X] or [O O O]
    * Two diagonals [X X X] or [O O O]
    :param state: the state of the current board
    :param player: a human or a computer
    :return: True if the player wins
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells


def valid_move(x, y):
    """
    A move is valid if the chosen cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the board[x][y] is empty
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def would_win(move, state, player):
    temp_s = deepcopy(state)
    temp_s[move[0]][move[1]] = player
    return wins(temp_s, player)


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def get_best_move(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = get_best_move(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    Print the board on console
    :param state: current state of the board
    """

    counter = 1
    print('----------------')
    for row in state:
        print('\n----------------')
        for cell in row:
            if cell == +1:
                print('|', c_choice, '|', end='')
            elif cell == -1:
                print('|', h_choice, '|', end='')
            else:
                print('|', counter, '|', end='')
            counter += 1
    print('\n----------------')


def ai_turn(c_choice, h_choice, player_choice):
    """
    It calls the minimax function if the depth < 9,
    else it choices a random coordinate.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f"{player_choice.name}'s turn [{c_choice}]")
    render(board, c_choice, h_choice)

    if depth == 9:
        x = random.choice([0, 1, 2])
        y = random.choice([0, 1, 2])
        set_move(x, y, COMP)
        return

    best_move = get_best_move(board, depth, COMP)
    chance = random.randint(1, 100)

    move = None
    if chance <= player_choice.optimal_percent or would_win(best_move, board, COMP):
        move = best_move
        player_choice.optimal_moves += 1
    else:
        e_cells = empty_cells(board)
        move = e_cells[random.randint(0, len(e_cells) - 1)]

    print(f"Chance: {chance}\n{player_choice.name}'s optimal percent: {player_choice.optimal_percent}")
    print(f"Chose optimal choice: {move == best_move}", "\n")

    x, y = move[0], move[1]
    set_move(x, y, COMP)
    player_choice.total_moves += 1
    time.sleep(1)


def human_turn(c_choice, h_choice):
    """
    The Human plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    print('Your turn [{}]'.format(h_choice))
    render(board, c_choice, h_choice)

    while (move < 1 or move > 9):
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            try_move = set_move(coord[0], coord[1], HUMAN)

            if try_move == False:
                print('Bad move')
                move = -1
        except KeyboardInterrupt:
            print('Bye')
            exit()
        except:
            print('Bad choice')


def get_player_lookup(players):
    return {player.name.lower(): player for player in players}


def get_player_choice(player_lookup):
    u_choice = ''

    print("Who do you want to play?")
    for name in player_lookup.keys():
        print(f"- {name.capitalize()}")

    while(not u_choice.lower() in player_lookup):
        try:
            u_choice = input("\nEnter their name: ")
            if not u_choice.lower() in player_lookup:
                print("invalid player")
        except:
            print("bad choice")
    return player_lookup[u_choice.lower()]


def create_players(player_csv):
    with open(player_csv) as csv_file:
        players = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        isThisTheHeader = False
        for row in csv_reader:
            if not isThisTheHeader:
                isThisTheHeader = True
            else:
                player = Player_Ai(name=row[0], optimal_percent=int(
                    row[3]), optimal_moves=int(row[1]), total_moves=int(row[2]))
                players.append(player)
    return players

# This method takes in the player object and updates the CSV with the latest data from the object at the time of being called.


def update_players_csv(player):

    newPlayerData = [player.name.lower(), player.optimal_moves,
                     player.total_moves, player.optimal_percent]

    with open('CSVFolder/player.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        lines = list(reader)
        for i in range(1, len(lines)):
            if lines[i][0] == player.name.lower():
                lines[i] = newPlayerData

    with open('CSVFolder/player.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

    readFile.close()
    writeFile.close()


def main():
    """
    Main function that calls all functions
    """
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    player_choice = ''  # selected player_choice
    first = ''  # if human is the first

    players = create_players("CSVFolder/player.csv")
    player_lookup = get_player_lookup(players)
    player_choice = get_player_choice(player_lookup)

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except KeyboardInterrupt:
            print('Bye')
            exit()
        except:
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except KeyboardInterrupt:
            print('Bye')
            exit()
        except:
            print('Bad choice')

    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice, player_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice, player_choice)

    # Game over message
    if wins(board, HUMAN):
        clean()
        print('Your turn [{}]'.format(h_choice))
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        clean()
        print(f"{player_choice.name}'s turn [{c_choice}]")
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')

    update_players_csv(player_choice)

    exit()


if __name__ == '__main__':
    main()
