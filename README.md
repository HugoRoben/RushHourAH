# Rush Hour

## Introduction
RushHourAH is a Python-based solver for the Rush Hour puzzle gam. This project aims to implement and compare various algorithms to find solutions for different configurations of the Rush Hour game, a popular sliding block puzzle. Users can execute the solver with different algorithms, visualize the results, and analyze performance metrics. The primary objective is to move vehicles in a grid to free the red blocked vehicle and lead it to the exit by taking the least amount of steps.

## Description

An in-depth paragraph about your project and overview of use.

## Installation
To install RushHourAH, follow these steps:
```bash
1. Clone the repository to your local machine.
git clone [https://github.com/HugoRoben/RushHourAH.git]
cd RushHourAH
2. Install the required libraries:
pip install -r requirements.txt

### Requirements
- Each experiment is run using a Macbook Pro 13 inch 
- Python 3
- Libraries: `tqdm`, `matplotlib`, `numpy`, `pygame` (See `requirements.txt` for more details)


### Executing program

## Usage
The project can be run from the command line. Here are some example commands:

python main.py [file_type] [algorithm] [additional options]
Replace [file_type] with csv or txt, [algorithm] with the chosen algorithm (e.g., Astar, IDDFS, BFS, Random), and include any additional options as needed, such as the dimension of the board or the amount of iterations.
- Run BFS algorithm for a specific range of games:
python main.py txt bfs --game_range '0-2'
- Run A* algorithm for a single game:
python main.py txt Astar --single_game 1
- Repeat a game multiple times using the Random algorithm:
python main.py txt Random --single_game 1 --repeat 10

## Features
- Multiple solving algorithms: A*, IDDFS, BFS, Random.
- Support for different game board dimensions.
- Repeat execution for statistical analysis.
- Visualization of solving process and results.
- Performance metrics and statistics

## Contributors
This project has been developed and maintained by Joeri den Heijer, Hugo Röben and Mina Bibi.

## License
RushHourAH is open source and free to use.