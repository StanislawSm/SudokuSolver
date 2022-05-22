import numpy as np

GRID_SIZE = 9
BLOCK_SIZE = 3

class Sudoku:
    def __init__(self, path_to_grid):
        self.grid = np.loadtxt(path_to_grid, dtype=int)
        assert self.grid.shape[0] == self.grid.shape[1] == GRID_SIZE, "Unsupported grid shape"

    def __str__(self):
        ret = ''
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i, j] == 0:
                    ret += '_'
                else:
                    ret += str(self.grid[i, j])
                if (j+1) == GRID_SIZE and (i+1) != GRID_SIZE:
                    ret += '\n'
                elif (j+1) % GRID_SIZE == 0:
                    ret += '  '
                else:
                    ret += ' '
            if (i+1) % GRID_SIZE == 0 and (i+1) != GRID_SIZE:
                ret += '\n'
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
        tmp = self.grid[row_idx, col_idx]
        self.grid[row_idx, col_idx] = num 
        ret = self.validate_grid()
        self.grid[row_idx, col_idx] = tmp
        return ret



def _is_field_valid(field):
    """
    Checks if a row, column or block has any duplicates

    field is a list of elements in a row, column or block

    Return True if valid, False otherwise
    """
    field = list(filter(lambda n: n != 0, field))
    return len(field) == len(set(field)) 


def solve_backtracking(sudoku):
    row, col = sudoku.get_empty_cell()
    
    # No empty cells i.e. solved
    if row == col == None:
        return True
    
    for n in range(1, 10):
        if sudoku.is_fill_legal(row, col, n):
            sudoku.grid[row, col] = n
            if solve_backtracking(sudoku):
                return True
            else:
                sudoku.grid[row, col] = 0

    return False
