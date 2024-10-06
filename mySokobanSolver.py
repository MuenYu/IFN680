'''
IFN680 Sokoban Assignment

The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

You are not allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and triggers to a fail for the test of your code.
'''


import search
import sokoban
from collections import deque

def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    e.g.  [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    '''

    return [
        (11457571, 'Muen', 'Yu'),
        (11491205, 'Danny', 'Jeong')
    ]
 

def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo' if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable.  
    When determining the taboo cells, you must ignore all the existing boxes, 
    simply consider the walls and the target cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner inside the warehouse and not a target, 
             then it is a taboo cell.
     Rule 2: all the cells between two corners inside the warehouse along a 
             wall are taboo if none of these cells is a target.
    
    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with 
       an '#' and the taboo cells marked with an 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    # Get the dimensions of the warehouse
    X, Y = zip(*warehouse.walls)
    x_size, y_size = 1 + max(X), 1 + max(Y)
    
    # Initialize the grid with spaces
    grid = [[" "] * x_size for _ in range(y_size)]
    
    # Mark the walls
    walls = set(warehouse.walls)
    for (x, y) in walls:
        grid[y][x] = "#"
    
    # Create a set of target coordinates for easier lookup
    targets = set(warehouse.targets)
    
    # Helper function to find interior cells using flood-fill
    def find_interior():
        interior = set()
        to_check = deque([warehouse.worker])
        
        while to_check:
            x, y = to_check.popleft()
            if (x, y) not in interior and (x, y) not in walls:
                interior.add((x, y))
                # Add adjacent cells to check
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    next_x, next_y = x + dx, y + dy
                    if 0 <= next_x < x_size and 0 <= next_y < y_size:
                        to_check.append((next_x, next_y))
        
        return interior

    # Get the interior cells
    interior_cells = find_interior()
    
    taboo = set()

    # Rule 1: Find corner cells in interior (ignoring targets)
    for x, y in interior_cells:
        if (x, y) not in targets:
            # Check if cell is a corner
            adjacent_walls = sum([(x-1, y) in walls, (x+1, y) in walls, 
                                  (x, y-1) in walls, (x, y+1) in walls])
            if adjacent_walls >= 2:
                # Confirm it's a corner by checking diagonal walls
                if ((x-1, y) in walls and (x, y-1) in walls) or \
                   ((x-1, y) in walls and (x, y+1) in walls) or \
                   ((x+1, y) in walls and (x, y-1) in walls) or \
                   ((x+1, y) in walls and (x, y+1) in walls):
                    taboo.add((x, y))
    
    # Rule 2: Find cells between corners along walls
    for y in range(1, y_size-1):
        row_taboo_cells = []
        for x in range(1, x_size-1):
            if (x, y) in walls:
                row_taboo_cells = []  # Reset if we encounter a wall
            elif (x, y) in taboo:  # Found a corner
                if row_taboo_cells:  # Check cells between corners
                    wall_above = all((xx, y-1) in walls for xx, yy in row_taboo_cells)
                    wall_below = all((xx, y+1) in walls for xx, yy in row_taboo_cells)
                    if (wall_above or wall_below) and all((xx, yy) not in targets for xx, yy in row_taboo_cells):
                        taboo.update(row_taboo_cells)
                row_taboo_cells = []  # Reset after processing
            else:
                row_taboo_cells.append((x, y))
    
    # Repeat for columns (vertical walls)
    for x in range(1, x_size-1):
        col_taboo_cells = []
        for y in range(1, y_size-1):
            if (x, y) in walls:
                col_taboo_cells = []  # Reset if we encounter a wall
            elif (x, y) in taboo:  # Found a corner
                if col_taboo_cells:  # Check cells between corners
                    wall_left = all((x-1, yy) in walls for xx, yy in col_taboo_cells)
                    wall_right = all((x+1, yy) in walls for xx, yy in col_taboo_cells)
                    if (wall_left or wall_right) and all((xx, yy) not in targets for xx, yy in col_taboo_cells):
                        taboo.update(col_taboo_cells)
                col_taboo_cells = []  # Reset after processing
            else:
                col_taboo_cells.append((x, y))

    # Mark taboo cells
    for (x, y) in taboo:
        grid[y][x] = "X"
    
    # Convert grid to string
    return "\n".join(["".join(line) for line in grid])


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. It uses search.Problem as a sub-class. 
    That means, it should have a:
    - self.actions() function
    - self.result() function
    - self.goal_test() function
    See the Problem class in search.py for more details on these functions.
    
    Each instance should have at least the following attributes:
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.
    
    
    '''
    
    def __init__(self, warehouse):
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        raise NotImplementedError


def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall, or walk into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using elementary actions 
    the puzzle defined in a file.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

def solve_sokoban_macro(warehouse):
    '''    
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

