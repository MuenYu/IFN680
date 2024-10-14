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
├───launcher: source code for a multi-thread sokoban solver launcher
├───efficiencyTest.py: used to test the efficiency of sokoban solver
├───mySokobanSolver.py: the sokoban solver
├───testlib.py: testing algorithm implementation
├───search.py: search algorithm implementation
└───sokoban.py: the definition of warehouse and solver
```

## How to Run Natively

Run Functional Test

```bash
python ./funcTest.py
```

Run Efficiency Test

```bash
python ./efficiencyTest.py
```

## How to Run with `launcher`

`launcher` is a program to run multiple sokoban solver simultaneously, written in Golang, utilizes the potential of
modern multiple
core processor. Developed for IFN680 testing, it can output the test result to the specified file.

`launcher` is a binary program, you need to run the version with matched suffix. (e.g. `win` or `mac`)

```cmd
./launcher-win.exe -macro=true -algorithm=astar -timeout=30m -output="./data.xlsx" 
```

It means for each sokoban puzzle, you will apply astar for searching algorithm and macro mode. Each task should be done
in 30 minutes, otherwise will be regarded as timeout. All test results will be output to `data.xlsx`

use `launcher -h` to check more usage