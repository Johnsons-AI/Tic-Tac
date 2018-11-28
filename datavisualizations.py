import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def read_in_csv(file_name):
	return pd.read_csv(file_name)

def create_visualizations(dataframe):
    dataframe.plot.bar(x='Name', y='total_moves_count', figsize=(8, 8))
    plt.xlabel('Names')
    plt.ylabel('Total Moves')
    plt.savefig('Visualizations/total_move_bar_plot.png')
    plt.clf()
    dataframe.plot.bar(x='Name', y='optimal_moves_count', figsize=(8, 8))
    plt.xlabel('Names')
    plt.ylabel('Optimal Moves')
    plt.savefig('Visualizations/optimal_move_bar_plot.png')
    plt.clf()
    dataframe.plot.bar(x='Name',
                y=['optimal_moves_count',
                'total_moves_count'], figsize=(8, 8)
                )
    plt.xlabel('Names')
    plt.ylabel('Total Moves VS Optimal Moves')
    plt.savefig('Visualizations/total_moves_vs_optimal_moves.png')
    # Create Pie Charts
    plt.clf()
    dataframe['actual_percent'] =  (dataframe['optimal_moves_count']/dataframe['total_moves_count']) * 100
    dataframe['actual_percent'] = pd.to_numeric(dataframe['actual_percent'], downcast='signed')
    dataframe.plot.bar(x='Name',
                       y=['actual_percent', 'predicted_percentage'], figsize=(8, 8)
                       )
    plt.xlabel('Names')
    plt.ylabel('Actual Percent VS Predicted Percent')
    plt.savefig('Visualizations/actual_percent_vs_predicted_percentage.png')
    # Create Pie Charts
    plt.clf()
    for i in range(len(dataframe.index)):
        total_moves = dataframe.iloc[i]['total_moves_count']
        optimal_moves = dataframe.iloc[i]['optimal_moves_count']
        plt.xlabel(dataframe.iloc[i]['Name'] + ' Total Moves VS Optimal Moves')
        plt.pie([total_moves - optimal_moves, optimal_moves], autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.3)
        plt.legend(['Total Moves', 'Optimal Moves'], loc='upper right')
        plt.savefig('Visualizations/' + dataframe.iloc[i]['Name'] + '_piechart.png')
        plt.clf()




def main():
	dataframe = read_in_csv('CSVFolder/player.csv')
	create_visualizations(dataframe)
	print(dataframe.head())

if __name__ == '__main__':
	main()	
