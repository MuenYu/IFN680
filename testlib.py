import glob
import time
from sokoban import Warehouse
from mySokobanSolver import *

def test_warehouse(problem_file, macro = False):
    '''
    This function will test the performance of your warehouse for either macro or elem solutions and return the result.
    You can check if this solution works with your gui, or by cleverly using the check_action_seq function.
    '''

    wh = Warehouse()
    wh.load_warehouse(problem_file)

    if macro:
        student_answer =  solve_sokoban_macro(wh)
    else:
        student_answer = solve_sokoban_elem(wh)
        
    return student_answer

def test_taboo_cells():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_0001.txt")
    expected_answer = '####  \n#X #  \n#  ###\n#   X#\n#   X#\n#XX###\n####  '
    answer = taboo_cells(wh)
    fcn = test_taboo_cells    
    print('<<  Testing {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)