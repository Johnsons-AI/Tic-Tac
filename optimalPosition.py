import csv
from minimax import render
from minimax import empty_cells as get_empty_cells
from minimax import would_win
from minimax import wins
from minimax import get_best_move
from random import randint


def generate_board(pieces, user_first=False, max_attempts=3,  attempt=1):
    """
    Generate a random board with no wins. 
    The computer is 1 and the user is -1.

    Arguments:
        pieces {int} -- number of desired pieces on board

    Keyword Arguments:
        user_first {bool} -- is user making first move (default: {False})
        max_attempts {int} -- max number of attempts to generate board (default: {3})
        attempt {int} -- current attempt at generating board (default: {1})

    Raises:
        AssertionError -- "Board must have 9 pieces or less."
        AssertionError -- "Reached max number of attempts."

    Returns:
        [int][int] -- board with desired config
    """

    assert pieces <= 9, "Board must have 9 pieces or less."
    assert attempt <= max_attempts, "Reached max number of attempts."

    first_player = -1 if user_first else 1
    second_player = -first_player

    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    for i in range(1, pieces+1):
        current_player = first_player if i % 2 != 0 else second_player

        # if no move could be found try again with a new board else set current player piece
        try:
            move = get_non_win_move(board, current_player)
        except ValueError as v_e:
            return generate_board(pieces, user_first, max_attempts, attempt + 1)
        else:
            board[move[0]][move[1]] = current_player

    return board


def get_non_win_move(board, player_value):
    """
    Get move that will not result in winning

    Arguments:
        board {[int][int]} -- current state of board
        player_value {int} -- player to find move for, 1 or -1

    Raises:
        ValueError -- Every possible move will result in a win.

    Returns:
        [int] -- possible non-winning move, row:move[0] col:move[1]
    """

    e_cells = get_empty_cells(board)
    found_move = False
    move = None

    while True:
        e_rand_index = randint(0, len(e_cells) - 1)
        move = e_cells.pop(e_rand_index)
        found_move = not would_win(move, board, player_value)

        if found_move or not e_cells:
            break

    if found_move:
        return move
    else:
        raise ValueError("Every possible move will result in a win.")


# Given a string of current board config, function opens csv file, makes a dictionary, & gets value from dict with current board position
def create_board_dict(fileName):
    with open(fileName) as csv_file:
        optimalDict = {}
        optimalDictConverted = {}

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'{row[0]}\t{row[1]}\t\t\t\t{row[2]}\t')
                line_count += 1
            else:
                # print(f'{row[0]}\t{row[1]}\t{row[2]}\t')
                temp = f'{row[2]}'
                temp_list = [int(temp[1]), int(temp[4])]

                optimalDict[f'{row[1]}'] = temp_list
                line_count += 1

        # converting optimalDict to int keys
        for boardConfig in optimalDict:

            # converting string from leron's csv file to list of lists for render parameter
            bareString = boardConfig.replace('[', '').replace(
                ']', '').replace(',', '').replace(' ', '')

            bareStrList = list(bareString)
            fullNumList = []

            i = 0
            while i < len(bareStrList):
                if bareStrList[i] == '-' or bareStrList == '+':
                    tempS = bareStrList[i] + bareStrList[i + 1]
                    tempI = int(tempS)
                    fullNumList.append(tempI)
                    i += 2
                else:
                    tempS = bareStrList[i]
                    tempI = int(tempS)
                    fullNumList.append(tempI)
                    i += 1

            # converted list for key use
            finalTuple = get_tuple_board(fullNumList)

            tempList = optimalDict[boardConfig]

            optimalDictConverted[finalTuple] = tempList

        return(optimalDictConverted)


def create_player_csv(boards):
    with open('CSVFolder/player.csv', 'a', newline='') as s:
        fileWriter = csv.writer(s)
        csv_dict = [row for row in csv.DictReader('CSVFolder/player.csv')]
        if len(csv_dict) == 0:
            fileWriter.writerow(
                ['Name', 'optimal_moves_count', 'total_moves_count', 'predicted_percentage'])

        flag = 'y'
        playerSymbol = 'X'

        while flag == 'y':
            userCorrect = 0
            total = 0
            stateCount = 0

            move = -1
            moves = {
                1: (0, 0), 2: (0, 1), 3: (0, 2),
                4: (1, 0), 5: (1, 1), 6: (1, 2),
                7: (2, 0), 8: (2, 1), 9: (2, 2),
            }

            print('Hey, I want to learn how you play.\nI need you give me a few inputs based on certain tic tac toe board scenarios.\n')
            playerName = input('Enter your name: ')

            for board, best_move in boards.items():
                total += 1
                render(board, 'O', 'X')

                print('\n You are the player using', playerSymbol)
                move = int(input('\n Use numpad (1..9): '))

                # counts correct answers
                if best_move == moves[move]:
                    userCorrect += 1

            # correct percentage
            predictPercent = (userCorrect / total) * 100

            # truncates decimal
            finalPercent = int(predictPercent)

            print()
            print(playerName, ', you got ', finalPercent,
                  '% ', 'of the answers correct')
            print('You got ', userCorrect, ' out of ', total, ' correct\n')

            fileWriter.writerow([playerName.lower(), 0, 0, finalPercent])

            flag = input(
                'Would you like to add a person for me to learn from? (y/n): ').lower()


def get_tuple_board(board):
    return tuple([tuple(row) for row in board])


def is_even(num):
    return num % 2 == 0
     

def get_random_boards(amount, min=1, max=6):
    boards = {}
    for _ in range(amount):
        pieces = randint(min, max)
        first = randint(0,1)
        
        # make sure the user actually has the next turn
        if first and not is_even(pieces):
            pieces = pieces + 1 if pieces == min else pieces - 1
        elif not first and is_even(pieces):
            pieces = pieces -1 if pieces == max else pieces + 1

        board = None
        tuple_board = None

        while True:
            try:
                board = generate_board(pieces, first)
            except AssertionError as ae:
                print(ae)
            else: 
                tuple_board = get_tuple_board(board)

            if not tuple_board in boards:
                break

        best_move = get_best_move(board, 9 - pieces, -1)
        best_move.pop()
        boards[tuple_board] = tuple(best_move)
    
    return boards


def main():
    # boards = create_board_dict('CSVFolder/SampleBoards.csv')
    boards = get_random_boards(10)
    create_player_csv(boards)


if __name__ == '__main__':
    main()
