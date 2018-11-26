import csv
from minimax import render

#Given a string of current board config, function opens csv file, makes a dictionary, & gets value from dict with current board position
def create_board_dict(fileName):
    with open(fileName) as csv_file:
        optimalDict = {}

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
        return(optimalDict)

def create_player_csv(boards):
    # TODO @Zane: create player csv
    with open ('create_player.csv', 'w', newline='') as s:
        fileWriter = csv.writer(s)

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
        
            print ('Hey, I want to learn how you play. \n I need you give me a few inputs based on certain tic tac toe board scenarios.\n')
            playerName = input('Enter your name: ')

            optimalBoardDict = boards


            for boardConfig in optimalBoardDict:
                total += 1
            
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
                for s in range(3, 6):
                    list2.append(fullNumList[s]) 
                for s in range(6, 9):
                    list3.append(fullNumList[s])    

                #converted list for key use
                finalList = [list1, list2, list3]


                render(finalList, 'O', 'X')
            
                print('\n')
                move = int(input('You are the player using X. \n Use numpad (1..9): '))
                
                #counts correct answers
                if optimalBoardDict[boardConfig] == moves[move]:
                    userCorrect += 1
                
            
            
            #correct percentage
            predictPercent = (userCorrect / total) * 100

            #truncates decimal
            finalPercent = int(predictPercent)

            print(finalPercent)

            fileWriter.writerow([playerName, finalPercent, 0, 0])

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
