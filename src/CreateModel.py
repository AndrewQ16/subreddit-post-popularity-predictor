import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Activation, Conv2D, MaxPooling2D, Flatten, Input, Embedding, LSTM
#Dense is a final fully connected output layer
import pickle
import datetime
import sys

def catDogClassificationModel():
    #Use Dropout

    #Look for signs of what seems to work so use hyperparameters:
    dense_layers = [0]

    #Might want to try smaller value since the images are resized to 70x70
    layer_sizes = [256] #If too high, will take forever. The counting is just convention
    conv_layers =[4]

    #Switch to the data directory
    os.chdir("data")

    IMG_SIZE = int(sys.argv[1])

    X = pickle.load(open("X{}.pickle".format(IMG_SIZE), "rb"))
    y = pickle.load(open("y{}.pickle".format(IMG_SIZE), "rb"))

    y = np.array(y)
    print("Y shape:")
    print(y.shape)
    exit()

    img_size = X[0].shape

    # #bring the data in and normalize (max is 255)
    X = np.array(X/255.0)
    y = np.array(y)

    for dense_layer in dense_layers:
        for layer_size in layer_sizes:
            for conv_layer in conv_layers:
                NAME = "{}-conv-{}-nodes-{}-dense-{}-img_size-softmax-{}".format(conv_layer, layer_size, dense_layer,IMG_SIZE, datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
                tensorboard = tf.keras.callbacks.TensorBoard(log_dir="log/{}".format(NAME))
                print("-------- NAME: " + NAME + ". END NAME------------")
                # Window is 3x3
                model = Sequential()
                # https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D
                # layer_Size = filters, 
                model.add(Conv2D(layer_size, (3, 3), activation='relu', input_shape=X.shape[1:]))
                model.add(MaxPooling2D((2, 2)))

                for l in range(conv_layer - 1):
                    model.add(Conv2D(layer_size, (3, 3), activation='relu'))
                    model.add(MaxPooling2D((2, 2)))

                model.add(Flatten()) #this converts our 3D feature maps to 1D feature vectors
                model.add(Dropout(0.5))
                for l in range(dense_layer):
                    model.add(Dense(64, activation='relu'))
                model.add(Dense(2, activation='softmax'))

                model.compile(optimizer='adam',
                            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                            metrics=['accuracy'])

        
                #batchsize 20-300 is a good range
                model.fit(X, y, batch_size=30,epochs=10, validation_split=0.1)

                
                os.chdir("../models")
                #Save the model here:
                
                model.save(NAME)
                #Move the directory back to pointing where data is
                os.chdir("../data")

def fullModel():

    print("-------------------------------------------------------")

    dense_layers = [0]
    layer_sizes = [256] 
    conv_layers =[4]

    #Switch to the data directory
    os.chdir("data")
    IMG_SIZE = int(sys.argv[1])

    # Load in data
    images = pickle.load(open("reddit_images-{}.pickle".format(IMG_SIZE), "rb"))
    captions = pickle.load(open("reddit_captions.pickle", "rb"))
    scores = pickle.load(open("reddit_scores.pickle", "rb"))
    
    # bring the data in and normalize images (max is 255)
    images = np.array(images)
    images = np.array(images/255.0)
    captions = np.array(captions)
    scores = np.array(scores)

    # Split all the data here
    train_size = int(0.8 * len(images))
    #valid_size = int(0.2 * len(images))
    
    img_train = images[:train_size,:]
    img_valid = images[train_size:,:]

    print("Img train size: {}".format(len(img_train)))
    print("Img validation size: {}".format(len(img_valid)))
    print("Img train shape: {}".format(img_train.shape))
    print("Img validation shape: {}".format(img_valid.shape))


    cap_train = captions[:train_size,:]
    cap_valid = captions[train_size:,:]

    print("Cap train size: {}".format(len(cap_train)))
    print("Cap validation size: {}".format(len(cap_valid)))
    print("Cap train shape: {}".format(cap_train.shape))
    print("Cap validation shape: {}".format(cap_valid.shape))
    
    scores = scores.reshape(len(images), 1)
    scores_train = scores[:train_size,:]
    scores_valid = scores[train_size:,:]

    print("Score train size: {}".format(len(scores_train)))
    print("Score validation size: {}".format(len(scores_valid)))
    print("Score train shape: {}".format(scores_train.shape))
    print("Score validation shape: {}".format(scores_valid.shape))
    print("----------------------------------------------")


    # Set up image layers here:
    image_input = Input(shape=images.shape[1:], name='image_input')
    NAME = ""
    img_output = None
    
    NAME = "merged-{}-conv-{}-nodes-{}-dense-{}-img_size-softmax-{}".format(4, 256, 0, IMG_SIZE, datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
    tensorboard = tf.keras.callbacks.TensorBoard(log_dir="logs/{}".format(NAME))
    print("-------- NAME: " + NAME + ". END NAME------------")
    
    # Window is 3x3 
    img_layer = Conv2D(256, (3, 3), activation='relu', input_shape=images.shape[1:]) (image_input)
    img_layer = MaxPooling2D((2, 2)) (img_layer)

    for l in range(2):
        img_layer = Conv2D(128, (3, 3), activation='relu') (img_layer)
        img_layer = MaxPooling2D((2, 2)) (img_layer)
    
    img_layer = Flatten() (img_layer) #this converts our 3D feature maps to 1D feature vectors
    img_layer = Dropout(0.5) (img_layer)
    for l in range(1):
        img_layer = Dense(64, activation='relu') (img_layer)

                
    img_output = Dense(10, activation='softmax') (img_layer)
                
    
    # Set up caption layers here:
    # captions are each of length 65
    caption_input = Input(shape=captions.shape[1:], name='caption_input')
    # input_dim found from printing out the length of each np array
    cap = Embedding(output_dim=128, input_dim=train_size, input_length=65) (caption_input)
    lstm_out = LSTM(32)(cap)
    
    layers = tf.keras.layers.concatenate([img_layer, lstm_out])


    layers = Dense(64, activation='relu') (layers)
    layers = Dense(64, activation='relu') (layers)
    layers = Dense(64, activation='relu') (layers)

    main_output = Dense(1, activation='relu', name = 'cap_output') (layers)

    model = Model(inputs=[image_input, caption_input], outputs=[img_output, main_output])

    model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), loss_weights=[1.,0.2])

    arr = np.arange(9862)

    model.fit([img_train, cap_train], [arr,scores_train], epochs=10, batch_size = 32)

    os.chdir("../models")
    #Save the model here:
    model.save(NAME)



def testLen():

    print("---")
    #Switch to the data directory
    os.chdir("data")
    IMG_SIZE = int(sys.argv[1])

    # Load in data
    images = pickle.load(open("reddit_images-{}.pickle".format(IMG_SIZE), "rb"))
    captions = pickle.load(open("reddit_captions.pickle", "rb"))
    scores = pickle.load(open("reddit_scores.pickle", "rb"))
    
    # bring the data in and normalize images (max is 255)
    images = np.array(images)
    images = np.array(images/255.0)

    # print("Images shape:")
    # print(images.shape)
    # print("Image ex:")
    # print(images)

    captions = np.array(captions)
    print("Captions shape:")
    print(captions.shape)
    print("Captions ex:")
    print(captions)

    scores = np.array(scores)
    print("Scores shape:")
    print(scores.shape)
    print("Scores ex:")
    print(scores)

    # Split all the data here
    # train_size = int(0.8 * len(images))
    # #valid_size = int(0.2 * len(images))
    
    # img_train = images[:train_size,:]
    # img_valid = images[train_size:,:]

    # cap_train = captions[:train_size,:]
    # cap_valid = captions[train_size:,:]
    
    # scores = scores.reshape(len(images), 1)
    # scores_train = scores[:train_size,:]
    # scores_valid = scores[train_size:,:]


    # for entry in captions:
    #     print(len(entry))
    return


if __name__ == "__main__":
    # catDogClassificationModel()
    fullModel()
    # testLen()

    pass