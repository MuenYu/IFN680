# load everything needed for testing
from testlib import *
from mySokobanSolver import *
        
test_taboo_cells()
test_check_elem_action_seq()
test_solve_sokoban_elem()

all_warehouses = sorted(glob.glob('warehouses/*.txt'))

for problem_file in all_warehouses:
    print(f'Testing {problem_file}')
    s = time.time()
    a = test_warehouse(problem_file)
    print(f'Answer: {a}')
    print(f'Time taken: {time.time()-s :.3f} seconds')    