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

def scan_warehouse(warehouse):
    '''
    the main logic for taboo_cells, including steps:
    1. create a grid based on the maze
    2. check the inner space of the maze
    3. check rule1: corner taboo in the inner space
    4. check rule2: taboo on the line along the wall
    5. return an interior cell set, a taboo cell set and grid
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

    return interior_cells, taboo, grid

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
    # fetch the grid of the warehouse with taboo cells
    _, _, grid = scan_warehouse(warehouse)
    
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
        self.interior_cells, self.taboo_cells, _ = scan_warehouse(warehouse)
        self.initial = (warehouse.worker, tuple(warehouse.boxes))
        # walls won't change its position, use set to optimize performance
        self.walls = set(warehouse.walls)
        # target won't change its position, use set to optimize performance
        self.targets = set(warehouse.targets)
        # Possible directions (dx, dy) and corresponding movement descriptions
        self.directions = {
            'Left': (-1, 0),
            'Right': (1, 0),
            'Up': (0, -1),
            'Down': (0, 1)
        }
        self.history = set()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        worker, boxes = state
        # the places of boxes are confirmed, use set to optimize performance
        boxes = set(boxes)
        possible_actions = []

        if state in self.history:
            return possible_actions

        self.history.add(state)

        if self.macro:
            reachable = self.get_reachable_range(worker, boxes)
            # Generate macro actions: Worker must be next to a box, and move that box.
            for (box_x, box_y) in boxes:
                for direction, (dx, dy) in self.directions.items():
                    next_worker_pos = (box_x - dx, box_y - dy)
                    # is the new position reachable? can u push the box there?
                    if next_worker_pos in reachable and self.is_valid_elem_move(direction, (box_x, box_y), boxes):
                        possible_actions.append(((box_y, box_x), direction))
        else:
            # Elementary actions: Worker moves by one step
            for direction, (dx, dy) in self.directions.items():
                next_worker_pos = (worker[0] + dx, worker[1] + dy)

                # Check if the worker can move without obstacles
                if self.is_valid_elem_move(direction, next_worker_pos, boxes):
                    possible_actions.append(direction)
        return possible_actions

    def result(self, state, action):
        """
        Returns the resulting state after applying the given action to the given state.
        """
        worker, boxes = state
        # the places of boxes are confirmed, use set to optimize performance
        boxes = set(boxes)

        if self.macro:
            # Macro action: push a box
            (box_y, box_x), direction = action
            dx, dy = self.directions[direction]
            new_box_pos = (box_x + dx, box_y + dy)
            new_worker_pos = (box_x, box_y)

            # # Update box position
            boxes.remove((box_x, box_y))
            boxes.add(new_box_pos)

            return new_worker_pos, tuple(boxes)
        else:
            # Elementary action: move worker
            direction = action
            dx, dy = self.directions[direction]
            new_worker_pos = (worker[0] + dx, worker[1] + dy)

            # If the worker pushes a box, move the box as well
            if new_worker_pos in boxes:
                new_box_pos = (new_worker_pos[0] + dx, new_worker_pos[1] + dy)
                boxes.remove(new_worker_pos)
                boxes.add(new_box_pos)

            return new_worker_pos, tuple(boxes)


    def goal_test(self, state):
        """
        Returns True if the given state is a goal state.
        The goal state is when all boxes are on target cells.
        """
        _, boxes = state
        return all(box in self.targets for box in boxes)

    def is_valid_elem_move(self, direction, next_pos, boxes):
        """
        Check if the elementary movement valid
        direction: the moving direction
        next_pos: the position of worker after moving
        boxes: list of boxes
        """
        if next_pos in self.walls:
            return False
        if next_pos in boxes:
            x, y = next_pos
            dx, dy = self.directions[direction]
            new_box = (x+dx, y+dy)
            # you cannot push two boxes or push a box to a wall
            if new_box in boxes or new_box in self.walls:
                return False
            # you cannot push a box to taboo cell
            if not self.allow_taboo_push and new_box in self.taboo_cells:
                return False
        return True

    def get_reachable_range(self, worker, boxes):
        '''
        return a set including all reachable locations for current worker and boxes
        '''
        queue = deque([worker])
        visited = {worker}

        while queue:
            cur_pos = queue.popleft()

            for _, (dx, dy) in self.directions.items():
                next_pos = (cur_pos[0] + dx, cur_pos[1] + dy)

                if next_pos not in visited and next_pos not in self.walls and next_pos not in boxes:
                    visited.add(next_pos)
                    queue.append(next_pos)
        return visited

    def h(self, state):
        '''
        heuristic function for A*
        return the sum of manhattan distance between boxes and the closest target
        '''
        worker, boxes = state.state

        # 1. Calculate the sum of the minimum matching distances between boxes and targets
        total_box_target_distance = 0
        boxes = list(boxes)
        targets = list(self.targets)

        # Calculate the minimum matching distance using Manhattan distance
        distances = []
        for box in boxes:
            box_distances = []
            for target in targets:
                box_distances.append(abs(box[0] - target[0]) + abs(box[1] - target[1]))
            distances.append(box_distances)

        # Use a greedy approximation to find minimum matching between boxes and targets
        while boxes and targets:
            # Find the box-target pair with the minimum distance
            min_distance = float('inf')
            min_box_idx, min_target_idx = -1, -1
            for i, box_distances in enumerate(distances):
                for j, distance in enumerate(box_distances):
                    if distance < min_distance:
                        min_distance = distance
                        min_box_idx = i
                        min_target_idx = j

            # Add the minimum distance to the total distance
            total_box_target_distance += min_distance

            # Remove the selected box and target from further consideration
            boxes.pop(min_box_idx)
            targets.pop(min_target_idx)
            distances.pop(min_box_idx)
            for box_distances in distances:
                box_distances.pop(min_target_idx)

        # 2. Calculate the distance from the worker to the closest box
        worker_to_box_distances = [abs(worker[0] - box[0]) + abs(worker[1] - box[1]) for box in boxes]
        worker_distance = min(worker_to_box_distances) if worker_to_box_distances else 0

        # Heuristic value is the sum of the distances and the penalty
        return total_box_target_distance + worker_distance


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
    solver = SokobanPuzzle(warehouse)
    state = solver.initial

    for action in action_seq:
        possible_actions = solver.actions(state)
        if action not in possible_actions:
            return 'Failure'
        state = solver.result(state,action)

    # Update warehouse with the new positions and return the result
    worker, boxes = state
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
    
    solver = SokobanPuzzle(warehouse)
    solution = search.breadth_first_graph_search(solver)
    
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
    solver = SokobanPuzzle(warehouse)
    y, x = dst
    reachable = solver.get_reachable_range(warehouse.worker, set(warehouse.boxes))
    return (x,y) in reachable

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
    solver = SokobanPuzzle(warehouse)
    solver.macro = True
    solution = search.breadth_first_graph_search(solver)
    
    if solution is None:
        return 'Impossible'
    else:
        return solution.solution()

