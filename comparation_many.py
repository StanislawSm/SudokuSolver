import StaSmy.test_one
from sudoku import Sudoku
from StaSmy.test_one import solve_sudoku_from_npArray
from timeit import default_timer as timer
from StaSmy.data_preprocess import get_data
import matplotlib.pyplot as plt

x_train, x_test, y_train, y_test = get_data('StaSmy/sudoku.csv')

numbers = [1, 2, 5, 8, 12, 15, 20]
backtrackingTime = [0] * len(numbers)
constraintTime = [0] * len(numbers)
antTime = [0] * len(numbers)
NNTime = [0] * len(numbers)

for number in numbers:
    print(number, " starting")
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
    print(number, " done")

plt.yscale("log")
plt.plot(numbers, backtrackingTime, label="backtracking")
plt.plot(numbers, constraintTime, label="constraints")
plt.plot(numbers, antTime, label="ant algorithm")
plt.plot(numbers, NNTime, label="neural network")
plt.title("algorithms comparison")
plt.xlabel("number of problems")
plt.ylabel("summary time needed [s]")
plt.legend()
plt.savefig("algCompLog.png")
plt.show()









