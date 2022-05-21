import numpy as np
import sys

class Sudoku:
    grid_size = 9
    block_size = 3

    def __init__(self, path_to_grid):
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

    '''
    checks if a row, a column or a block has any duplicates
    field is a list of elements in row, column or block
    return True if valid, False otherwise
    '''
    @staticmethod
    def is_field_valid(field):
        field = list(filter(lambda n: n != 0, field))
        return len(field) == len(set(field))

    '''
    checks every row, column and block for duplicates
    return True if a grid is valid, False otherwise
    '''
    def validate_grid(self):
        # every row
        for i in range(self.grid_size):
            if not self.is_field_valid(self.grid[i, :].tolist()):
                return False

        # every column
        for j in range(self.grid_size):
            if not self.is_field_valid(self.grid[:, i].tolist()):
                return False

        # every cell
        for i in range(0, self.grid_size, self.block_size):
            for j in range(0, self.grid_size, self.block_size):
                if not self.is_field_valid(self.grid[i:i+self.block_size, j:j+self.block_size].flatten().tolist()):
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


def main():
    sudoku = Sudoku(sys.argv[1])


if __name__ == '__main__':
    main()
