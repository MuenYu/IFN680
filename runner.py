import argparse
import json

from mySokobanSolver import *
from sokoban import *
from search import *
import time

parser = argparse.ArgumentParser()
parser.add_argument('--macro', type=bool)
parser.add_argument('--taboo', type=bool)
parser.add_argument('--house', type=str)
parser.add_argument('--algorithm', type=str)

args = parser.parse_args()

house = Warehouse()
house.load_warehouse(args.house)
solver = SokobanPuzzle(house, macro=args.macro, allow_taboo_push=args.taboo)

start = time.time()
solution = None
if args.algorithm == 'astar':
    solution = astar_graph_search(solver)
else:
    solution = breadth_first_graph_search(solver)
duration = time.time() - start

result = {
    'duration': duration,
    'solution': 'Impossible' if solution is None else str(solution.solution())
}

print(json.dumps(result))
