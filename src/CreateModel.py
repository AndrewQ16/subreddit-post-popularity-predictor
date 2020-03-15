import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Conv2D, MaxPooling2D, Flatten
#Dense is a final fully connected output layer

import pickle

X = pickle.load(open("X.pickle", "rb"))

y = pickle.load(open("y.pickle", "rb"))

#bring the data in and normalize (max is 255)

X = np.array(X/255.0)
y = np.array(y)

model = Sequential()
#32 or any value would be fine. Window is 3x3
model = Sequential()
model.add(Conv2D(64, (3, 3), activation='relu', input_shape=X.shape[1:]))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))

model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(10))

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

#batchsize 20-300 is a good range
model.fit(X, y, batch_size=32,epochs=10, validation_split=0.1)



