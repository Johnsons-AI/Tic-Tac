import csv
from minimax import render

#Given a string of current board config, function opens csv file, makes a dictionary, & gets value from dict with current board position
def create_board_dict(fileName):
    with open(fileName) as csv_file:
        optimalDict = {}
        optimalDictConverted = {}

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'{row[0]}\t{row[1]}\t\t\t\t{row[2]}\t')
                line_count += 1
            else:
                #print(f'{row[0]}\t{row[1]}\t{row[2]}\t')
                temp = f'{row[2]}'
                temp_list = [int(temp[1]), int(temp[4])]
                
                optimalDict[f'{row[1]}'] = temp_list
                line_count += 1
        
        
        #converting optimalDict to int keys
        for boardConfig in optimalDict:
            
                #converting string from leron's csv file to list of lists for render parameter
                bareString = boardConfig.replace('[', '').replace(']', '').replace(',', '').replace(' ', '')

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

                #converted list for key use
               # finalList = [list1, list2, list3]
                finalTuple = (tuple1, tuple2, tuple3)

                tempList = optimalDict[boardConfig]

                optimalDictConverted[finalTuple] = tempList

        return(optimalDictConverted)

def create_player_csv(boards):
    # TODO @Zane: create player csv
    with open ('CSVFolder/player.csv', 'w', newline='') as s:
        fileWriter = csv.writer(s)

        fileWriter.writerow(['Name', 'optimal_moves_count', 'total_moves_count', 'predicted_percentage'])

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
        
            print ('Hey, I want to learn how you play.\nI need you give me a few inputs based on certain tic tac toe board scenarios.\n')
            playerName = input('Enter your name: ')

            boardDict = boards

            for currBoard in boardDict:
                total += 1

                #rendering board for user
                render(currBoard, 'O', 'X')
            
                print('\n')
                move = int(input('You are the player using X. \n Use numpad (1..9): '))
                
                #counts correct answers
                if boardDict[currBoard] == moves[move]:
                    userCorrect += 1
                
            
            
            #correct percentage
            predictPercent = (userCorrect / total) * 100

            #truncates decimal
            finalPercent = int(predictPercent)

            print()
            print(playerName, ', you got ', finalPercent, '% ', 'of the answers correct')
            print('You got ', userCorrect, ' out of ', total, ' correct\n')
            

            fileWriter.writerow([playerName, 0, 0, finalPercent])

            flag = input('Would you like to add a person for me to learn from? (y/n): ').lower()
  
'''
#Test to see if dictionary prints out the correct optimal position
def test():
    fileName = 'SampleBoards.csv'
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:        
                test = optimalMove('SampleBoards.csv')
                print(test[f'{row[1]}'])
                line_count += 1
'''

def main():
    boards = create_board_dict('CSVFolder/SampleBoards.csv')
    create_player_csv(boards)
    

if __name__ == '__main__':
    main()
