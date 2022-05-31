import StaSmy.test_one
from sudoku import Sudoku
from StaSmy.test_one import solve_sudoku_from_npArray
from timeit import default_timer as timer
from StaSmy.data_preprocess import get_data

x_train, x_test, y_train, y_test = get_data('StaSmy/sudoku.csv')

numbers = [1, 20, 50, 100, 1000, 2000, 5000]
backtrackingTime = [0] * len(numbers)
constraintTime = [0] * len(numbers)
antTime = [0] * len(numbers)
NNTime = [0] * len(numbers)

for number in numbers:
    for i in range(0, number):
        sudokuBacktracking = Sudoku("sample_data/sudoku1.txt")
        sudokuBacktracking.grid = StaSmy.test_one.denorm(x_train[i]).reshape(9, 9).astype(int)

        sudokuConstraints = Sudoku("sample_data/sudoku1.txt")
        sudokuConstraints.grid = StaSmy.test_one.denorm(x_train[i]).reshape(9, 9).astype(int)

        sudokuAnt = Sudoku("sample_data/sudoku1.txt")
        sudokuAnt.grid = StaSmy.test_one.denorm(x_train[i]).reshape(9, 9).astype(int)

        sudokuNN = Sudoku("sample_data/sudoku1.txt")
        sudokuNN.grid = StaSmy.test_one.denorm(x_train[i]).reshape(9, 9).astype(int)

        start = timer()
        sudokuBacktracking.solve_backtracking()
        end = timer()
        backtrackingTime[numbers.index(number)] += end - start

        start = timer()
        sudokuConstraints.solve_backtracking()
        end = timer()
        constraintTime[numbers.index(number)] += end - start

        start = timer()
        sudokuAnt.solve_backtracking()
        end = timer()
        antTime[numbers.index(number)] += end - start

        start = timer()
        solve_sudoku_from_npArray(sudokuNN.grid)
        end = timer()
        NNTime[numbers.index(number)] += end - start

print(backtrackingTime)
print(constraintTime)
print(antTime)
print(NNTime)







