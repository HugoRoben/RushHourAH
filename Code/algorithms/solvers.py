import time
import csv
from tqdm import tqdm
from Code.algorithms.IDDFS import *
from Code.classes.VehicleClass import Vehicle
from Code.classes.RushClass import RushHour
from Code.algorithms.Random import iterative_deepening_search
from Code.algorithms.BFS import breadth_first_search
from Code.algorithms.Astar import *

def load_game_data(args):
    """
    Loads game data based on specified file type and arguments.
    
    Args:
    ---------------------------------------------------------------------------
        Command line arguments or equivalent, containing file_type 
        and other relevant info.
    
    Returns:
    ---------------------------------------------------------------------------
        A generator yielding RushHour game instances, or None if loading fails.
    """
    
    file_type = args.file_type.lower()
    
    if file_type == 'csv':
        if not all([args.dimension, args.board_number]):
            print("Please specify both dimension and board number for CSV files.")
            return None
        file_path = f'boards/Rushhour{args.dimension}x{args.dimension}_{args.board_number}.csv'
        return load_csv_file(file_path, args.dimension)
        
    elif file_type == 'txt':
        if not (args.single_game or args.game_range or args.all_games):
            print("Please specify one of --single_game, --game_range, or --all_games for TXT files.")
            return None

        file_path = 'boards/Board_file.txt'
        try:
            with open(file_path, 'r') as file:
                total_games = sum(1 for _ in file)
            game_indices = get_game_indices(args, total_games)
            return load_txt_file(file_path, game_indices)
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            return None


def load_csv_file(rushhour_file, dimension) -> RushHour:
    """
    Loads Rush Hour game instances from a CSV file.
    
    Args:
    ---------------------------------------------------------------------------
        rushhour_file (str): The path to the CSV file.
        dimension (int): Dimension of the Rush Hour game board.
    
    Returns:
    ---------------------------------------------------------------------------
        Generator[RushHour, None, None]: A generator yielding RushHour game 
        instances.
    """
    
    vehicles = []
    with open(rushhour_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            id, orientation, x, y, length = row
            vehicles.append(Vehicle(id, orientation, int(x) - 1, int(y) - 1, int(length)))
    yield RushHour(set(vehicles), dimension)


def load_txt_file(file_path, game_indices: int, dimension: int =6) -> RushHour:
    """
    Loads Rush Hour games from a text file.
    
    Args:
    ---------------------------------------------------------------------------
        file_path (str): Path to the text file.
        game_indices (List[int]): List of game indices to load.
        dimension (int): The dimension of the game board, default is 6.
        
    Returns:
    ---------------------------------------------------------------------------
        Generator[RushHour, None, None]: A generator yielding RushHour game 
        instances.
    """
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i in game_indices:
        if i < len(lines):
            game_data = lines[i].strip()
            steps, board_config, num_configs = game_data.split()
            vehicle_positions = {}

            for j, char in enumerate(board_config):
                if char not in ['o', 'x']:
                    if char not in vehicle_positions:
                        vehicle_positions[char] = [j]
                    else:
                        vehicle_positions[char].append(j)

            vehicles = []
            for vehicle_id, positions in vehicle_positions.items():
                x, y = positions[0] % dimension, positions[0] // dimension
                length = len(positions)
                orientation = 'H' if positions[1] % dimension > positions[0] % dimension else 'V'

                vehicles.append(Vehicle(vehicle_id, orientation, x, y, length))

            yield RushHour(set(vehicles), dimension)


def get_game_indices(args, total_games: int) -> List[str]:
    """
    Determines game indices to load based on user arguments.
    
    Args:
    ---------------------------------------------------------------------------
        args: Command line arguments or equivalent.
        total_games (int): Total number of games available.
        
    Returns:
    ---------------------------------------------------------------------------
        List[int]: List of game indices to be loaded.
    """
    
    if args.all_games:
        return list(range(total_games))
    elif args.single_game is not None:
        return [args.single_game]
    elif args.game_range is not None:
        start, end = map(int, args.game_range.split('-'))
        return list(range(start, end + 1))


def solve_game(rush_game: RushHour, algorithm: str, max_depth: int =1000,\
                    max_iterations: int =1000000):
    """
    Solves a Rush Hour game using a specified algorithm.
    
    Args:
    ---------------------------------------------------------------------------
        rush_game (RushHour): The Rush Hour game to solve.
        algorithm (str): The name of the algorithm to use for solving.
        max_depth (int): Maximum depth for depth-related algorithms.
        max_iterations (int): Maximum iterations for iteration-based algorithms.
        
    Returns:
    ---------------------------------------------------------------------------
        Tuple[Optional[Dict[str, any]], int]: Tuple containing the solution 
        details and status code.
    """
    
    start_time = time.perf_counter()
    results = None

    if algorithm.lower() == 'astar':
        results = Astar(rush_game).astar_search(rush_game)
    elif algorithm.lower() == 'iddfs':
        results = iterative_deepening_search(rush_game, max_depth)
    elif algorithm.lower() == 'bfs':
        results = breadth_first_search(rush_game, max_depth)
    elif algorithm.lower() == 'random':
        results = random_solve_puzzle(rush_game, max_iterations)
    else:
        print("Invalid algorithm. Please choose from Astar, IDDFS, DFS, Random or BFS.")
        return None, 1

    end_time = time.perf_counter()
    if results and (results.get('solution')):
        solution = results.get('solution')
        visited = results.get('visited')
        steps = len(solution)
        return solution, {"steps": steps, "visited": visited, "time": end_time - start_time}, 0
    else:
        return {"steps": 0, "time": 0}, 1


def solve_rush_hour_games(rush_games: List[RushHour], algorithm: str, repeat: int):
    """
    Solves multiple Rush Hour games using the specified algorithm.
    
    Args:
    ---------------------------------------------------------------------------
        rush_games (Generator[RushHour, None, None]): Generator of Rush Hour games.
        algorithm (str): The algorithm to use for solving the games.
        repeat (int): Number of times to repeat solving each game.
        
    Returns:
    ---------------------------------------------------------------------------
        Tuple[Dict[str, List[float]], int, List[Optional[Dict[str, any]]]]: Tuple 
        containing statistics, the count of unsolved games, and the list of solutions.
    """
    
    stats = {"times": [], "steps": [], "visited": [],}
    unsolved_count = 0
    solutions = []
    game_count = 0 

    with tqdm(desc="Solving Games") as progress_bar:
        for game in rush_games:
            for _ in range(repeat):
                solutions, result, unsolved = solve_game(game, algorithm)
                stats["times"].append(result["time"])
                stats["steps"].append(result["steps"])
                stats["visited"].append(result["visited"])
                unsolved_count += unsolved
                game_count += 1
                progress_bar.update(1)
                progress_bar.set_description(f"Processed {game_count} games")

    return stats, unsolved_count, solutions
