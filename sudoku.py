import numpy as np
from constraint import *

GRID_SIZE = 9
BLOCK_SIZE = 3

class Sudoku:
    def __init__(self, path_to_grid):
        self.grid = np.loadtxt(path_to_grid, dtype=int)
        assert self.grid.shape[0] == self.grid.shape[1] == GRID_SIZE, "Unsupported grid shape"

    def __str__(self):
        ret = ""
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i, j] == 0:
                    ret += "_"
                else:
                    ret += str(self.grid[i, j])
                if (j+1) == GRID_SIZE and (i+1) != GRID_SIZE:
                    ret += "\n"
                elif (j+1) % BLOCK_SIZE == 0:
                    ret += "  "
                else:
                    ret += " "
            if (i+1) % BLOCK_SIZE == 0 and (i+1) != GRID_SIZE:
                ret += "\n"
        return ret

    def validate_grid(self):
        """
        Checks every row, column and block in a grid for duplicates

        Return True if valid, False otherwise
        """
        # every row
        for i in range(GRID_SIZE):
            if not _is_field_valid(self.grid[i, :].tolist()):
                return False

        # every column
        for i in range(GRID_SIZE):
            if not _is_field_valid(self.grid[:, i].tolist()):
                return False

        # every block
        for i in range(0, GRID_SIZE, BLOCK_SIZE):
            for j in range(0, GRID_SIZE, BLOCK_SIZE):
                if not _is_field_valid(self.grid[i:i+BLOCK_SIZE, j:j+BLOCK_SIZE].flatten().tolist()):
                    return False
        return True

    def get_empty_cell(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i, j] == 0:
                    return i, j
        return None, None

    def is_fill_legal(self, row_idx, col_idx, num):
        """
        Checks if a cell can be filled with a number
        """
        tmp = self.grid[row_idx, col_idx]
        self.grid[row_idx, col_idx] = num 
        ret = self.validate_grid()
        self.grid[row_idx, col_idx] = tmp
        return ret

    def solve_backtracking(self):
        """
        Solves sudoku using a backtracking method

        1. Assign a number to an empty cell
        2. Recursively check if this assignment leads to a solution
        3. If it doesn't - try the next number for the current cell
        """
        row, col = self.get_empty_cell()

        # No empty cells i.e. solved
        if row == col == None:
            return True

        for n in range(1, 10):
            if self.is_fill_legal(row, col, n):
                self.grid[row, col] = n
                if self.solve_backtracking():
                    return True
                else:
                    self.grid[row, col] = 0
            
        return False

    def solve_constraints(self):
        problem = Problem()

        # 9 rows of 9 variables, each variable rangin 1..9
        for i in range(1, 10):
            problem.addVariables(range(i*10 + 1, i*10 + 10), range(1, 10))

        # Each row has different values
        for i in range(1, 10):
            problem.addConstraint(AllDifferentConstraint(), range(i*10 + 1, i*10 + 10))
        
        # Each column has different values
        for i in range(1, 10):
            problem.addConstraint(AllDifferentConstraint(), range(i+10, 100+i, 10))

        # Each block has different values
        for i in [1, 4, 7]:
            for j in [1, 4, 7]:
                block = [((i+z)*10 + j+y) for z in range(0,BLOCK_SIZE) for y in range(0, BLOCK_SIZE)]
                problem.addConstraint(AllDifferentConstraint(), block)

        # Add init values
        for i in range(1, 10):
            for j in range(1, 10):
                if self.grid[i-1, j-1] != 0:
                    problem.addConstraint(
                        lambda var, val=self.grid[i-1, j-1]: var == val, (i*10 + j,)
                    )
        
        # Gather result
        solution = problem.getSolution()
        for i in range(1, 10):
            for j in range(1, 10):
                idx = i*10 + j
                self.grid[i-1, j-1] = solution[idx]

         

def _is_field_valid(field):
    """
    Checks if a row, column or block has any duplicates

    field is a list of elements in a row, column or block

    Return True if valid, False otherwise
    """
    field = list(filter(lambda n: n != 0, field))
    return len(field) == len(set(field)) 

