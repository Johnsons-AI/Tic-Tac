import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def read_in_csv(file_name):
	return pd.read_csv(file_name)

def create_visualizations(dataframe):
    plt.figure(figsize=(800,800))
    dataframe.plot.bar(x='Name', y='total_moves_count')
    plt.xlabel('Names')
    plt.ylabel('Total Moves')
    plt.savefig('Visualizations/total_move_bar_plot.png')
    plt.clf()
    dataframe.plot.bar(x='Name', y='optimal_moves_count')
    plt.xlabel('Names')
    plt.ylabel('Optimal Moves')
    plt.savefig('Visualizations/optimal_move_bar_plot.png')
    plt.clf()
    dataframe.plot.bar(x='Name',
                y=['optimal_moves_count',
                'total_moves_count']
                )
    plt.xlabel('Names')
    plt.ylabel('Total Moves VS Optimal Moves')
    plt.savefig('Visualizations/total_moves_vs_optimal_moves.png')
    # Create Pie Charts
    plt.clf()
    for i in range(len(dataframe.index)):
        total_moves = dataframe.iloc[i]['total_moves_count']
        optimal_moves = dataframe.iloc[i]['optimal_moves_count']
        plt.xlabel(dataframe.iloc[i]['Name'] + ' Total Moves VS Optimal Moves')
        plt.pie([total_moves - optimal_moves, optimal_moves], autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
        plt.legend(['Total Moves', 'Optimal Moves'], loc='upper right')
        plt.savefig('Visualizations/' + dataframe.iloc[i]['Name'] + '_piechart.png')
        plt.clf()




def main():
	dataframe = read_in_csv('mock_player_data.csv')
	create_visualizations(dataframe)
	print(dataframe.head())

if __name__ == '__main__':
	main()	
