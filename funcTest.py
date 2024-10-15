# load everything needed for testing
import time

from testlib import *
from mySokobanSolver import *
        
test_taboo_cells()
test_check_elem_action_seq()
test_solve_sokoban_elem()
test_can_go_there()
test_solve_sokoban_macro()

# start = time.time()
# a = test_warehouse('./warehouses/warehouse_0035.txt', macro=True)
# print(a)
# print(f'Time taken: {time.time()-start :.3f} seconds')
