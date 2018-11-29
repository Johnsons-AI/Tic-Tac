import csv
from minimax import render
from minimax import empty_cells as get_empty_cells
from minimax import would_win
from minimax import wins
import random


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
        e_rand_index = random.randint(0, len(e_cells) - 1)
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
            list1 = []
            list2 = []
            list3 = []

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
            for s in range(0, 3):
                list1.append(fullNumList[s])
                tuple1 = tuple(list1)
            for s in range(3, 6):
                list2.append(fullNumList[s])
                tuple2 = tuple(list2)
            for s in range(6, 9):
                list3.append(fullNumList[s])
                tuple3 = tuple(list3)

            # converted list for key use
           # finalList = [list1, list2, list3]
            finalTuple = (tuple1, tuple2, tuple3)

            tempList = optimalDict[boardConfig]

            optimalDictConverted[finalTuple] = tempList

        return(optimalDictConverted)


def create_player_csv(boards):
    with open('CSVFolder/player.csv', 'w', newline='') as s:
        fileWriter = csv.writer(s)

        fileWriter.writerow(['Name', 'optimal_moves_count',
                             'total_moves_count', 'predicted_percentage'])

        flag = 'y'

        while flag == 'y':
            userCorrect = 0
            total = 0

            move = -1
            moves = {
                1: [0, 0], 2: [0, 1], 3: [0, 2],
                4: [1, 0], 5: [1, 1], 6: [1, 2],
                7: [2, 0], 8: [2, 1], 9: [2, 2],
            }

            print('Hey, I want to learn how you play.\nI need you give me a few inputs based on certain tic tac toe board scenarios.\n')
            playerName = input('Enter your name: ')

            boardDict = boards

            for currBoard in boardDict:
                total += 1

                # rendering board for user
                render(currBoard, 'O', 'X')

                print('\n')
                move = int(
                    input('You are the player using X. \n Use numpad (1..9): '))

                # counts correct answers
                if boardDict[currBoard] == moves[move]:
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


'''
#Test to see if dictionary prints out the correct optimal position
def test():
    fileName = 'CSVFolder/SampleBoards.csv'
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:        
                test = create_board_dict('CSVFolder/SampleBoards.csv')
                print(test[f'{row[1]}'])
                line_count += 1
'''


def main():
    # boards = create_board_dict('CSVFolder/SampleBoards.csv')
    # create_player_csv(boards)

    # TODO: take this out
    b = generate_board(pieces=9, max_attempts=10, user_first=False)
    valid = not wins(b, 1) or wins(b, -1)
    print("Number of pieces: 9")
    print(f"User piece: O")
    print(f"User first: False")
    print(f"No winner: {valid}")
    render(b, 'x', 'o')

    print("\n", '_' * 17, "\n")

    b = generate_board(pieces=9, max_attempts=10, user_first=True)
    valid = not wins(b, 1) or wins(b, -1)
    print("Number of pieces: 9")
    print(f"User piece: O")
    print(f"User first: True")
    print(f"No winner: {valid}")
    render(b, 'x', 'o')


if __name__ == '__main__':
    main()
