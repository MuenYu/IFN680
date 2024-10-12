# load everything needed for testing
from testlib import *
from mySokobanSolver import *
        
test_taboo_cells()
test_check_elem_action_seq()
test_solve_sokoban_elem()
test_can_go_there()
test_solve_sokoban_macro()

# house = Warehouse()
# house.load_warehouse('./warehouses/warehouse_0005.txt')
# print(solve_sokoban_macro(house))
# print(taboo_cells(house))