import keras
from model import get_model
from StaSmy.data_preprocess import get_data

x_train, x_test, y_train, y_test = get_data('sudoku.csv')

model = get_model()

adam = keras.optimizers.Adam(lr=.001)
model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)
    
model.fit(x_train, y_train, batch_size=32, epochs=2)
