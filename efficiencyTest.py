# load everything needed for testing
from mySokobanSolver import *
from testlib import *

all_warehouses = sorted(glob.glob('warehouses/*.txt'))

for problem_file in all_warehouses:
    print(f'Testing {problem_file}')
    s = time.time()
    a = test_warehouse(problem_file)
    print(f'Answer: {a}')
    print(f'Time taken: {time.time()-s :.3f} seconds')    
