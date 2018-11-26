import csv

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
    pass

def main():
    boards = create_board_dict('SampleBoards.csv')
    create_player_csv(boards)

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

main()

#test()


