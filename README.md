# Tic-Tac Human AI

## Description

A Tic-Tac-Toe AI that learns to play like a user by utilizing the Minimax algorithm! 

Our game will create a probability/difficulty score derived from when the user picks the most optimal move given game states. 
Then using that probability, we create an AI version of that player. It will either choose the best move or a random move when playing. 

For example, after training with Zane, our AI noticed Zane chooses the most optimal move 48% of the time. In return, the Zane-AI will choose the most optimal move around 48% of the time.


## The Approach 

### Training
- We generate a user desired amount of board states.
- Find the optimal position of those random boards using the Minimax algorithm.
- Ask the user to choose their next move given a state.
- Keep track of how many moves they made that agrees with the Minimax algorithm
- Generate their difficulty level from their total number of optimal-moves and their total moves/boards

### Playing
- Generate a probability that player ai (created above) would choose the best move
- If this probability is within that player Predicted Percentage (from training), play the best move
- If the next best/optimal move would make the ai win, play the best move
- Else choose a random empty position on the board.

## Results and Visualizations!
Upon completing the project we were able to compare our Optimal Moves to Total Moves and found several key data points. We also compared Predicted Percent to Actual Percent.

### Total Moves VS Opitmal Moves
![Screenshot](https://github.com/Johnsons-AI/Tic-Tac/blob/master/Visualizations/total_moves_vs_optimal_moves.png)

### Predicted Percent VS Actual Percent 
![Screenshot](https://github.com/Johnsons-AI/Tic-Tac/blob/master/Visualizations/actual_percent_vs_predicted_percentage.png)

### Sample Pie Chart
![Screenshot](https://github.com/Johnsons-AI/Tic-Tac/blob/master/Visualizations/zane_piechart.png)


# Tasks
https://docs.google.com/document/d/1S_aaCiO6XnPOngXmRHI8aEOCuMqlua_LpZ4VwkkUAsc/edit?usp=sharing

