import sys
from sudoku import Sudoku

sudoku = Sudoku(sys.argv[1])

print(sudoku)
print("--------------------")

sudoku.solve_backtracking()

print(sudoku)
print(sudoku.validate_grid())
