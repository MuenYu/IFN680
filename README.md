# IFN680 - sokoban solver

## Signs in warehouse
- `space`: free space
- `#`: a wall block
- `$`: a box
- `.`: a target square
- `@`: the player
- `!`: the player on a target square
- `*`: a box on a target square

## Folder Structure
```
├───warehouses: warehouse folder
├───funcTest.py: used to test the correctness of components of sokoban solver
├───efficiencyTest.py: used to test the efficiency of sokoban solver
├───mySokobanSolver.py: the sokoban solver
├───testlib.py: testing algorithm implementation
├───search.py: search algorithm implementation
└───sokoban.py: the definition of warehouse and solver
```

## How to Run
Run Functional Test
```bash
python ./funcTest.py
```

Run Efficiency Test
```bash
python ./efficiencyTest.py
```
