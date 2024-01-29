from Code.visual.visualizer import *
from ..Classes.RushClass import RushHour

def reconstruct_path(board: RushHour):
    path = []
    while board:
        path.append(board)
        board = board.parent
    return path[::-1]

def depth_First_Search(RushGame: RushHour, max_depth: int=500):
    Stack = [RushGame]
    number_of_nodes = 0
    archive = {RushGame}
    
    while Stack:
        current_board = Stack.pop()
        number_of_nodes += 1

        if current_board.move_count >= max_depth:
            continue

        if current_board.is_solved():
            solution_path = reconstruct_path(current_board)
            # visualizer = Visualizer(600, 600)
            # visualizer.animate_solution(solution_path)
            return {"nodes": number_of_nodes, "solution": solution_path}

        for new_board in current_board.moves():
            if new_board not in archive:
                new_board.parent = current_board
                archive.add(new_board)
                Stack.append(new_board)

    return {"nodes": number_of_nodes, "solutions": None}

