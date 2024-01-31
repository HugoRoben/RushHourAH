# Rush Hour

## Introduction
RushHourAH is a Python-based solver for the Rush Hour puzzle game. This project aims to implement and compare various algorithms to find solutions for different configurations of the Rush Hour game, a sliding block puzzle. Users can execute the solver with an Weighted A*, Breadth-first-search and an iterative deepening depth-first search algorithm. The solution can be visualized and animated in pygame. The primary objective is to move vehicles in a grid to free the red vehicle and lead it to the exit by taking the fewest steps.
In the game, vehicles can not move over each other or move out of their row/column.

## Description


## Installation
To install RushHourAH, follow these steps:
```bash
1. Clone the repository to your local machine.
git clone [https://github.com/HugoRoben/RushHourAH.git]
cd RushHourAH
2. Install the required libraries:
pip install -r requirements.txt
```

### Requirements
- Python 3
Libraries: See `requirements.txt` for the required packages

### Executing program

## Usage
The project can be run from the command line. Here are some example commands:
```bash
python main.py [file_type] [algorithm] [additional options]
Replace [file_type] with csv or txt, [algorithm] with the chosen algorithm (e.g., Astar, IDDFS, BFS, Random), and include any additional options as needed, such as the dimension of the board or the amount of iterations needed to solve the puzzle.
- Run BFS algorithm for a specific range of games from the txt file:
python main.py txt bfs --game_range '0-2'
- Run A* algorithm for a single game from the txt file:
python main.py txt Astar --single_game 1
- Repeat a game multiple times using the Random algorithm:
python main.py txt Random --single_game 1 --repeat 10

Commands used to print the results of each algorithm on the 6x6_3 board. (The random algorithms give incosistent results at each experiment so we repeat the experiment and use the mean value of the results):
- python3 main.py csv random --dimension 6 --board 3 --repeat 1000
- python3 main.py csv bfs --dimension 6 --board 3
- python3 main.py csv iddfs --dimension 6 --board 3
- python3 main.py csv astar --dimension 6 --board 3

We do the same for the 9x9_4 board, by replacing the  --dimension 6 --board 3 parts with  --dimension 9 --board 4.

Example commands on the bfs algorithm:
- python3 main.py txt bfs --game_range '0-2'
- python3 main.py txt bfs --single_game 1
- python3 main.py txt bfs --single_game 1 --repeat 2
- python3 main.py txt bfs --all_games
- python3 main.py txt bfs --single_game 1 --repeat 10
- python3 main.py txt bfs --all_games --repeat 5
- python3 main.py csv bfs --dimension 6 --board 3
- python3 main.py csv bfs --dimension 6 --board 3 --repeat 5
```

## Features
- Solving algorithms: Weighted A*, IDDFS, BFS, Random.
- Support for different game board dimensions.
- Repeat execution for statistical analysis.
- Visualization of solving process and results.
- Performance metrics and statistics

### Breadth-First-Search:
BFS algorithm starts with the initial configuration of the board. It uses a queue to manage the exploration of game states, with the starting state being enqueued first. It keeps track of all visited states to prevent revisiting them.

At each step, BFS dequeues the state at the front of the queue, generates all possible next states from legal moves, and enqueues these new states if they haven't been visited before. For every state, BFS checks if the state is a solution to the game, until a solution is found.

### Iterative Deepening Depth-First Search
IDDFS starts at the initial board configuration and explores states using depth-first search, with an increasing depth limit in each iteration. It goes into the game tree up to the depth limit. If no solution is found, it backtracks and deepens the search in the next iteration. This process continues until it finds the shortest solution.

### Weighted A*
The weighted A* algorithm begins with the initial board state and evaluates nest states based on a cost function. This cost is built out of the number of cars blocking the red car, the length of these cars, and the distance to the exit. The total cost is then calculated with different weights, depending on the state of the board.
At each step, A* expands the lowest-cost node and explores its next states. The algorithm continues this process until it finds a path that leads the red car to the exit.

## Contributors
This project has been developed and maintained by Joeri den Heijer, Hugo Röben and Mina Bibi.

## License
RushHourAH is open source and free to use.