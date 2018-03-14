import numpy as np
import timeit


# Load sudokus
sudokus = np.load("resources/data/sudokus.npy")
oneksudokus = np.load("resources/data/sudoku-sample-1000.npy")

# Load solutions
solutions = np.load("resources/data/solutions.npy")


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.
    Input
        sudoku : 9x9 numpy array of integers
            Empty cells are designated by 0.
    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    # Generate list of solutions for each position
    dict = generate_dictionary(sudoku)

    # If a single position is empty, return np.full((9,9),-1)
    for key in dict:
        if not dict[key]:
            return np.full((9,9),-1)

    # Try out all values using dictionary and backtracking
    sudoku_result = sudoku_backtrack_search(sudoku,dict)

    return sudoku_result


def generate_dictionary(sudoku):
    height, width = np.shape(sudoku)

    dict = {}

    for y in range(height):
        for x in range(width):
            if sudoku[y,x] != 0:
                continue
            possibleValues = []
            for value in range(1,10):
                if isPossibleSolution(sudoku, value, x, y):
                    possibleValues.append(value)
            dict[(x, y)] = possibleValues

    return dict


def sudoku_backtrack_search(sudoku,dictionary):
    # Find a blank spot to fill
    try:
        x, y = findBlankSpace(sudoku)
    # If no blank spots are found, its solved!
    except noBlanksFound:
        return sudoku

    # Store all possible solutions for this blank spot
    possible_solutions = dictionary[(x,y)]


    # Keep copy of current board on recursive stack
    solved_sudoku = np.copy(sudoku)

    # Try all possible solutions, backtracking where necessary
    for value in possible_solutions:
        try:
            if isPossibleSolution(solved_sudoku, value, x, y):
                # print("TRY", value, "FOR [ x:", x, "|", "y:", y, "] FROM:", possible_solutions)
                solved_sudoku[y, x] = value
                return sudoku_backtrack_search(solved_sudoku,dictionary)
            else:
                continue
        except noSolutionFound:
            # print("failed")
            continue

    raise noSolutionFound()


def findBlankSpace(sudoku):
    height, width = np.shape(sudoku)
    for y in range(height):
        for x in range(width):
            if sudoku[y, x] == 0:
                return x, y
    raise noBlanksFound('No blank space found')


def isPossibleSolution(sudoku, value, xCoord, yCoord):
    # Initialize height & width of puzzle
    height, width = np.shape(sudoku)

    # Row y must not contain value
    for x in range(width):
        if sudoku[yCoord,x] == value:
            return False

    # Column x must not contain value
    for y in range(height):
        if sudoku[y,xCoord] == value:
            return False

    # This 3x3 grid must not contain value
    gridY = yCoord - (yCoord % 3)
    gridX = xCoord - (xCoord % 3)

    # Check if this number is unique within this 3x3 grid
    for i in range(3):
        for j in range(3):
            if sudoku[gridY+i, gridX+j] == value:
                return False

    # If all tests passed, return True
    return True


class noBlanksFound(Exception):
    pass


class noSolutionFound(Exception):
    pass


# One thousand test

a = timeit.default_timer()
for i in range(1000):
    print(i)
    sudoku_solver(oneksudokus[i])
b = timeit.default_timer()
print("time taken:", (b-a))

# Dictionary test
"""
sudoku1 = sudokus[0]
print("Puzzle 1")
print(sudoku1)
print()
print("Generated Dictionary")
print(generate_dictionary(sudoku1))
"""

# Impossible test
"""
sudoku1 = sudokus[0];
sudoku1[1,0] = 7
print(sudoku1)
print(sudoku_solver(sudoku1))
"""

# Actual test
"""
a = timeit.default_timer()
for i in range(100):
    print("Puzzle",i,"result:",np.array_equal(sudoku_solver(sudokus[i]), solutions[i]))
b = timeit.default_timer()
print("time taken:", (b-a))
"""

# Puzzle test
"""
print("Actual Puzzle")
print(sudokus[0])
print()
print("Actual Solution")
print(solutions[0])
print()
print("Calculated Solution:")
print(sudoku_solver(sudokus[0]))
"""