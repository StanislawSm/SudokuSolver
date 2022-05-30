from sudoku import Sudoku
from StaSmy.test_one import solve_sudoku_from_npArray
from timeit import default_timer as timer


sudokuBacktracking = Sudoku("sample_data/sudoku1.txt")
sudokuConstraints = Sudoku("sample_data/sudoku1.txt")
sudokuAnt = Sudoku("sample_data/sudoku1.txt")
sudokuNN = Sudoku("sample_data/sudoku1.txt")

print(sudokuBacktracking)


print("backtracking algorithm")
start = timer()
sudokuBacktracking.solve_backtracking()
end = timer()
print("time: ", end - start)
print("solved:", sudokuBacktracking.validate_grid())

print()
print("constraints algorithm")
start = timer()
sudokuConstraints.solve_constraints()
end = timer()
print("time: ", end - start)
print("solved:", sudokuConstraints.validate_grid())

print()
print("ant algorithm")
start = timer()
sudokuAnt.solve_aco()
end = timer()
print("time: ", end - start)
print("solved:", sudokuAnt.validate_grid())

print()
print("neural network algorithm")
start = timer()
solve_sudoku_from_npArray(sudokuNN.grid)
end = timer()
print("time: ", end - start)
print("solved:", sudokuNN.validate_grid())
