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
                
        def solve_aco(self):
        pom = True
        while pom:
            pom = False
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if self.grid[i, j] == 0:
                        possibleNumbers = []
                        for n in range(1, 10):
                            if self.is_fill_legal(i, j, n):
                                possibleNumbers.append(n)
                        if len(possibleNumbers) == 1:
                            n = possibleNumbers.pop(0)
                            self.grid[i, j] = n
                            pom = True
        solver = SudokuSolver(10)
        solver.Solve(self.grid)
        self.grid = solver.bestSol

         

def _is_field_valid(field):
    """
    Checks if a row, column or block has any duplicates

    field is a list of elements in a row, column or block

    Return True if valid, False otherwise
    """
    field = list(filter(lambda n: n != 0, field))
    return len(field) == len(set(field)) 

class SudokuSolver:
    q0 = 0.9
    rho = 0.9
    bestEvap = 0.005
    bestVal = 0
    bestPher = 0.0
    bestSol = []
    pheronomeMatrix = []
    antList = []
    pher0 = 1 / 81
    randomDist = random.random()

    def __init__(self, numAnts):
        self.numberAnts = numAnts
        for i in range(numAnts):
            self.antList.append(Ant(self))

    def Solve(self, grid):
        solved = False
        iter = 0
        bestPher = 0.0
        curBestAnt = 0
        self.InitPhermone()
        while not solved:
            for ant in self.antList:
                ant.InitSolution(grid, random.randrange(0, (GRID_SIZE**2)-1))
            for i in range(GRID_SIZE**2):
                for ant in self.antList:
                    ant.StepSolution()
            iBest = 0
            bestVal = 0
            for i in range(len(self.antList)):
                if self.antList[i].NumCellsFilled() > self.bestVal:
                    bestVal = 0
                    for j in range(GRID_SIZE):
                        for k in range(GRID_SIZE):
                            if self.antList[i].sol[j, k] != 0:
                                bestVal+=1
                    iBest = i
            pherToAdd = (GRID_SIZE**2)/(1+(GRID_SIZE**2)-bestVal)
            if bestVal<GRID_SIZE**2:
                pherToAdd = GRID_SIZE**2/((GRID_SIZE**2)-bestVal)
            else:
                pherToAdd = pherToAdd
            if pherToAdd > bestPher:
                self.bestSol = self.copyGrid(self.antList[iBest].sol)
                bestPher = pherToAdd
                curBestAnt = bestVal
                if bestVal == GRID_SIZE**2:
                    solved = True
            self.UpdatePhermone()
            bestPher = bestPher * (1.0 - self.bestEvap)
            iter+=1
        return solved

    def LocalPhermoneUpdate(self, iCell, iChoice):
        self.pheronomeMatrix[iCell, iChoice] = self.pheronomeMatrix[iCell, iChoice] * 0.9 + self.pher0 * 0.1

    def InitPhermone(self):
        pher = []
        for i in range(GRID_SIZE ** 2):
            r = []
            for j in range(GRID_SIZE):
                r.append(self.pher0)
            pher.append(r)
        self.pheronomeMatrix = pher

    def UpdatePhermone(self):
        for i in range(GRID_SIZE**2):
            col = i % 9
            row = int(i / 9)
            self.bestSol = np.array(self.bestSol)
            self.pheronomeMatrix = np.array(self.pheronomeMatrix)
            if self.bestSol[row, col]!=0:
                indeks = self.bestSol[row, col] - 1
                self.pheronomeMatrix[i, indeks] = self.pheronomeMatrix[i, indeks] * (1.0 - self.rho) + self.rho * self.bestPher
    def copyGrid(self, grid):
        grid = np.array(grid)
        res = []
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                row.append(grid[i, j])
            res.append(row)
        return res

class Ant:
    iCell = 0
    roulette = []
    rouletteVals = []
    sol = []
    failCells = 0

    def __init__(self, parent):
        self.parent = parent

    def copyGrid(self, grid):
        grid = np.array(grid)
        res = []
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                row.append(grid[i, j])
            res.append(row)
        return res

    def InitSolution(self, grid, startCell):
        self.sol = self.copyGrid(grid)
        self.iCell = startCell
        self.failCells = 0
        self.roulette = []
        self.rouletteVals = []
        for i in range(GRID_SIZE):
            self.rouletteVals.append(0)
            self.roulette.append(0.0)

    def NumCellsFilled(self):
        ret = GRID_SIZE**2 - self.failCells
        return ret

    def isFillLegal(self, row_idx, col_idx, num, grid):
        tmp = grid[row_idx, col_idx]
        grid[row_idx, col_idx] = num
        ret = self.validate_grid(grid)
        grid[row_idx, col_idx] = tmp
        return ret

    def validate_grid(self, grid):
        # every row
        for i in range(GRID_SIZE):
            if not _is_field_valid(grid[i, :].tolist()):
                return False

        # every column
        for i in range(GRID_SIZE):
            if not _is_field_valid(grid[:, i].tolist()):
                return False

        # every block
        for i in range(0, GRID_SIZE, BLOCK_SIZE):
            for j in range(0, GRID_SIZE, BLOCK_SIZE):
                if not _is_field_valid(grid[i:i + BLOCK_SIZE, j:j + BLOCK_SIZE].flatten().tolist()):
                    return False
        return True

    def StepSolution(self):
        col = self.iCell % 9
        row = int(self.iCell / 9)
        self.sol = np.array(self.sol)
        if self.sol[row, col] == 0:
            self.failCells += 1
            choice =[]
            for n in range(1, GRID_SIZE + 1):
                if self.isFillLegal(row, col, n, self.sol):
                    choice.append(n)
            if self.parent.randomDist > self.parent.q0:
                best = 0
                maxPher = -1.0
                self.parent.pheronomeMatrix = np.array(self.parent.pheronomeMatrix)
                for n in choice:
                    if self.parent.pheronomeMatrix[self.iCell, n - 1] > maxPher:
                        maxPher = self.parent.pheronomeMatrix[self.iCell, n - 1]
                        best = n
                self.sol[row, col] = best
                self.parent.LocalPhermoneUpdate(self.iCell, best - 1)
            else:
                totPher = 0.0
                numChoices = 0
                self.roulette = np.array(self.roulette)
                self.rouletteVals = np.array(self.rouletteVals)
                self.parent.pheronomeMatrix = np.array(self.parent.pheronomeMatrix)
                for n in choice:
                    toSet = totPher+self.parent.pheronomeMatrix[self.iCell, n - 1]
                    self.roulette[numChoices] = toSet
                    totPher = self.roulette[numChoices]
                    self.rouletteVals[numChoices] = n
                    numChoices+=1
                rouletteVal = totPher * self.parent.randomDist

                for i in range(numChoices):
                    if self.roulette[i]>rouletteVal:
                        self.sol[row, col] = self.rouletteVals[i]
                        self.parent.LocalPhermoneUpdate(self.iCell, self.rouletteVals[i] - 1)
                        break
        self.iCell+=1
        if self.iCell == GRID_SIZE**2:
            self.iCell=0

