import numpy as np
import copy

class Sudoku:
    def __init__(self, path_to_grid, grid_size=9, block_size=3):
        self.grid_size = grid_size
        self.block_size = block_size
        self.grid = np.loadtxt(path_to_grid, dtype=int)
        assert self.grid.shape[0] == self.grid.shape[1] == self.grid_size, 'Unsupported grid shape'

    def __str__(self):
        ret = ''
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i, j] == 0:
                    ret += '_'
                else:
                    ret += str(self.grid[i, j])
                if (j+1) == self.grid_size and (i+1) != self.grid_size:
                    ret += '\n'
                elif (j+1) % self.block_size == 0:
                    ret += '  '
                else:
                    ret += ' '
            if (i+1) % self.block_size == 0 and (i+1) != self.grid_size:
                ret += '\n'
        return ret

    def validate_grid(self):
        '''
        Checks every row, column and block in a grid for duplicates

        Return True if valid, False otherwise
        '''
        # every row
        for i in range(self.grid_size):
            if not _is_field_valid(self.grid[i, :].tolist()):
                return False

        # every column
        for i in range(self.grid_size):
            if not _is_field_valid(self.grid[:, i].tolist()):
                return False

        # every cell
        for i in range(0, self.grid_size, self.block_size):
            for j in range(0, self.grid_size, self.block_size):
                if not _is_field_valid(self.grid[i:i+self.block_size, j:j+self.block_size].flatten().tolist()):
                    return False
        return True

    def solve_brute_force(self):
        # TODO
        pass

    def solve_genetic(self):
        # TODO
        pass

    def solve_backtracing(self):
        # TODO
        pass


def _is_field_valid(field):
    '''
    Checks if a row, column or block has any duplicates

    field is a list of elements in a row, column or block

    Return True if valid, False otherwise
    '''
    field = list(filter(lambda n: n != 0, field))
    return len(field) == len(set(field))

def is_fill_legal(sudoku, row_idx, col_idx, num):
    '''
    Checks if a cell can be filled with a number legally
    '''
    sudoku_copy = copy.deepcopy(sudoku)
    sudoku_copy.grid[row_idx, col_idx] = num
    return sudoku_copy.validate_grid()


