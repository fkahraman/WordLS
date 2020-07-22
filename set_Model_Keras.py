"""
        Author : Fatih Kahraman
        Mail   : fatih.khrmn@hotmail.com
"""

import numpy as np
from sklearn.model_selection import train_test_split
import os
import matplotlib.pyplot as plt

from keras.utils import to_categorical

from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D, Flatten, BatchNormalization, MaxPool1D, LSTM, Bidirectional

data = np.loadtxt("DATA/data.csv", delimiter=' ')

X = data[:,:-1]
X = np.expand_dims(X, axis=2)

y = data[:,-1]

y = to_categorical(y)

#Splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=141, shuffle=True)

sequence_length = 50
nb_features = 15
nb_out = 1
valid_word_quantity = 160


# Simple CNN + RNN model
model = Sequential()

model.add(Conv1D(8, 1, input_shape=(15, 1), activation='relu'))

model.add(Conv1D(16, 6,activation='relu'))

model.add(Conv1D(32, 3,activation='relu'))

model.add(Conv1D(64, 3,activation='relu'))

model.add(Conv1D(128, 2,activation='relu'))

model.add(Conv1D(256, 2,activation='relu'))

model.add(Bidirectional(LSTM(4, input_shape=(512, 1))))

model.add(Dense(512, activation='relu'))
model.add(Dropout(0.25))

model.add(Dense(valid_word_quantity, activation='softmax'))

model.summary()

#opt = SGD(lr=0.01, momentum=0.9, decay=0.01)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=50, batch_size=512,  validation_data=[X_test, y_test])

# "Loss"#plt.plot(history.history['loss'])
#plt.plot(history.history['val_loss'])
#plt.title('model loss')
#plt.ylabel('loss')
#plt.xlabel('epoch')
#plt.legend(['train', 'validation'], loc='upper left')
#plt.show()

if not os.path.exists('MODEL/'):
    os.makedirs('MODEL/')

model_json = model.to_json()
with open("MODEL/model_ann.json", "w") as model_file:
    model_file.write(model_json)
# serialize weights to HDF5
model.save_weights("MODEL/ann_weights.h5")
