import sys
from sudoku import Sudoku

sudoku = Sudoku(sys.argv[1])

print(sudoku)
print("--------------------")

sudoku.solve_constraints()

print(sudoku)
print(sudoku.validate_grid())

