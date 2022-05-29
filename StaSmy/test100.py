import copy
import keras
import numpy as np
from data_preprocess import get_data

x_train, x_test, y_train, y_test = get_data('sudoku.csv')

model = keras.models.load_model('model/sudoku.model')


def norm(a):
    return (a / 9) - .5


def denorm(a):
    return (a + .5) * 9


def inference_sudoku(sample):
    # This function solve the sudoku by filling blank positions one by one.

    feat = copy.copy(sample)
    while True:
        out = model.predict(feat.reshape((1, 9, 9, 1)))
        out = out.squeeze()

        pred = np.argmax(out, axis=1).reshape((9, 9)) + 1
        prob = np.around(np.max(out, axis=1).reshape((9, 9)), 2)

        feat = denorm(feat).reshape((9, 9))
        mask = (feat == 0)

        if mask.sum() == 0:
            break

        prob_new = prob * mask

        ind = np.argmax(prob_new)
        x, y = (ind // 9), (ind % 9)

        val = pred[x][y]
        feat[x][y] = val
        feat = norm(feat)

    return pred


# testing 100 games
def test_accuracy(feats, labels):
    correct = 0
    for i, feat in enumerate(feats):

        pred = inference_sudoku(feat)
        true = labels[i].reshape((9, 9)) + 1

        if abs(true - pred).sum() == 0:
            correct += 1

    print(correct / feats.shape[0])


test_accuracy(x_test[:100], y_test[:100])


