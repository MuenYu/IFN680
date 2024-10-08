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
    interior_cells = set()

    # find all interior cells using BFS
    to_check = deque([warehouse.worker])
        
    while to_check:
        x, y = to_check.popleft()
        if (x, y) not in interior_cells and (x, y) not in walls:
            interior_cells.add((x, y))
            # Add adjacent cells to check
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < x_size and 0 <= next_y < y_size:
                    to_check.append((next_x, next_y))
    
    # The taboo cells set
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
                    no_target = all((xx, yy) not in targets for xx, yy in row_taboo_cells)
                    if (wall_above or wall_below) and no_target:
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
                    no_target = all((xx, yy) not in targets for xx, yy in col_taboo_cells)
                    if (wall_left or wall_right) and no_target:
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
        """
        Initializes the Sokoban puzzle.

        :param warehouse: A valid Warehouse object.
        :param macro: If True, use macro actions (moving boxes directly). If False, use elementary actions (worker moves).
        :param allow_taboo_push: If True, allow moves that push a box into a taboo cell. If False, such moves are not allowed.
        """
        self.warehouse = warehouse
        self.allow_taboo_push = False
        self.macro = False
        self.initial = (warehouse.worker, tuple(warehouse.boxes))

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        worker, boxes = state
        possible_actions = []

        # Possible directions (dx, dy) and corresponding movement descriptions
        directions = {
            'Left': (-1, 0),
            'Right': (1, 0),
            'Up': (0, -1),
            'Down': (0, 1)
        }

        if self.macro:
            # Generate macro actions: Worker must be next to a box, and move that box.
            for (box_x, box_y) in boxes:
                for direction, (dx, dy) in directions.items():
                    next_worker_pos = (box_x - dx, box_y - dy)
                    next_box_pos = (box_x + dx, box_y + dy)

                    # Check if the worker can move next to the box and push it in the valid direction
                    if self.is_valid_move(worker, next_worker_pos, boxes) and self.is_valid_move(boxes, next_box_pos, boxes):
                        if self.allow_taboo_push or next_box_pos not in taboo_cells(self.warehouse):
                            possible_actions.append(((box_x, box_y), direction))
        else:
            # Elementary actions: Worker moves by one step
            for direction, (dx, dy) in directions.items():
                next_worker_pos = (worker[0] + dx, worker[1] + dy)

                # Check if the worker can move without obstacles
                if self.is_valid_move(worker, next_worker_pos, boxes):
                    possible_actions.append(direction)

        return possible_actions

    def result(self, state, action):
        """
        Returns the resulting state after applying the given action to the given state.
        """
        worker, boxes = state
        boxes = list(boxes)

        if self.macro:
            # Macro action: push a box
            (box_x, box_y), direction = action
            dx, dy = {'Left': (-1, 0), 'Right': (1, 0), 'Up': (0, -1), 'Down': (0, 1)}[direction]
            new_box_pos = (box_x + dx, box_y + dy)
            new_worker_pos = (box_x, box_y)

            # Update box position
            boxes.remove((box_x, box_y))
            boxes.append(new_box_pos)

            return new_worker_pos, tuple(boxes)
        else:
            # Elementary action: move worker
            direction = action
            dx, dy = {'Left': (-1, 0), 'Right': (1, 0), 'Up': (0, -1), 'Down': (0, 1)}[direction]
            new_worker_pos = (worker[0] + dx, worker[1] + dy)

            # If the worker pushes a box, move the box as well
            if new_worker_pos in boxes:
                new_box_pos = (new_worker_pos[0] + dx, new_worker_pos[1] + dy)
                boxes.remove(new_worker_pos)
                boxes.append(new_box_pos)

            return new_worker_pos, tuple(boxes)


    def goal_test(self, state):
        """
        Returns True if the given state is a goal state.
        The goal state is when all boxes are on target cells.
        """
        _, boxes = state
        return all(box in self.warehouse.targets for box in boxes)


    def is_valid_move(self, worker, next_pos, boxes):
        """
        Check if a worker can move to the next position.
        """
        if next_pos in self.warehouse.walls:
            return False
        if next_pos in boxes:
            return False
        return True


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
    worker = warehouse.worker
    boxes = set(warehouse.boxes)
    walls = set(warehouse.walls)
    targets = set(warehouse.targets)

    directions = {
        'Left': (-1, 0),
        'Right': (1, 0),
        'Up': (0, -1),
        'Down': (0, 1)
    }

    for action in action_seq:
        dx, dy = directions[action]
        next_worker_pos = (worker[0] + dx, worker[1] + dy)

        if next_worker_pos in walls:
            return "Failure"

        if next_worker_pos in boxes:
            next_box_pos = (next_worker_pos[0] + dx, next_worker_pos[1] + dy)
            if next_box_pos in walls or next_box_pos in boxes:
                return "Failure"
            boxes.remove(next_worker_pos)
            boxes.add(next_box_pos)

        worker = next_worker_pos

    # Update warehouse with the new positions and return the result
    new_warehouse = warehouse.copy(worker=worker, boxes=boxes)
    return str(new_warehouse)


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
    
    sokoban_puzzle = SokobanPuzzle(warehouse)
    solution = search.breadth_first_graph_search(sokoban_puzzle)
    
    if solution is None:
        return 'Impossible'
    else:
        return solution.solution()


def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    sokoban_puzzle = SokobanPuzzle(warehouse, macro=False)
    problem = sokoban_puzzle.initial

    def is_reachable(problem, dst):
        frontier = deque([problem])
        explored = set()

        while frontier:
            current_state = frontier.popleft()
            worker, _ = current_state

            if worker == dst:
                return True

            if worker in explored:
                continue
            explored.add(worker)

            # Get all possible movements
            for action in sokoban_puzzle.actions(current_state):
                new_state = sokoban_puzzle.result(current_state, action)
                frontier.append(new_state)

        return False

    return is_reachable(problem, dst)

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
    sokoban_puzzle = SokobanPuzzle(warehouse)
    sokoban_puzzle.macro = True
    solution = search.breadth_first_graph_search(sokoban_puzzle)
    
    if solution is None:
        return 'Impossible'
    else:
        return solution.solution()

