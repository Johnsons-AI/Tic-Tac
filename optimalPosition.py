import csv

#Given a string of current board config, function opens csv file, makes a dictionary, & gets value from dict with current board position
def optimalMove(fileName):
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
                optimalDict[f'{row[1]}'] = list(f'{row[2]}'.split("[]"))
                line_count += 1
        return(optimalDict)

def main():
    optimalMove('SampleBoards.csv')



main()
