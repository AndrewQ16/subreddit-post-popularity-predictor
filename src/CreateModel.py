import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Conv2D, MaxPooling2D, Flatten
#Dense is a final fully connected output layer
import pickle
import datetime


#Use Dropout

#Look for signs of what seems to work so use hyperparameters:
dense_layers = [0,1,2]


#Might want to try smaller value since the images are resized to 70x70
layer_sizes = [32, 64, 128] #If too high, will take forever. The counting is just convention
conv_layers =[1,2,3]

#Switch to the data directory
os.chdir("data")

X = pickle.load(open("X.pickle", "rb"))
y = pickle.load(open("y.pickle", "rb"))



# #bring the data in and normalize (max is 255)
# X = np.array(X/255.0)
# y = np.array(y)

for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            NAME = "{}-conv-{}-nodes-{}-dense-{}".format(conv_layer, layer_size, dense_layer, datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
            tensorboard = tf.keras.callbacks.TensorBoard(log_dir="logs/{}".format(NAME))

            # Window is 3x3
            model = Sequential()
            model.add(Conv2D(layer_size, (3, 3), activation='relu', input_shape=X.shape[1:]))
            model.add(MaxPooling2D((2, 2)))

            for l in range(conv_layer - 1):
                model.add(Conv2D(layer_size, (3, 3), activation='relu'))
                model.add(MaxPooling2D((2, 2)))

            model.add(Flatten()) #this converts our 3D feature maps to 1D feature vectors

            for l in range(dense_layer):
                model.add(Dense(dense_layer, activation='relu'))

            model.add(Dense(10))

            model.compile(optimizer='adam',
                        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                        metrics=['accuracy'])

    
            #batchsize 20-300 is a good range
            model.fit(X, y, batch_size=16,epochs=10, validation_split=0.1, callbacks=[tensorboard])

            
            os.chdir("../models")
            #Save the model here:
            
            model.save(NAME)
            #Move the directory back to pointing where data is
            os.chdir("../data")
