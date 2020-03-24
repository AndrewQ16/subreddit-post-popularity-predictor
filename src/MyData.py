import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import random
import pickle

# translate = {"cane": "dog", "cavallo": "horse", "elefante": "elephant", "farfalla": "butterfly", 
#     "gallina": "chicken", "gatto": "cat", "mucca": "cow", "pecora": "sheep", 
#     "scoiattolo": "squirrel", "dog": "cane", "cavallo": "horse", "elephant" : "elefante", 
#     "butterfly": "farfalla", "chicken": "gallina", "cat": "gatto", "cow": "mucca", "spider": "ragno", 
#     "squirrel": "scoiattolo"}


#The size that images get set to. That means any images passed to the model must be of the same size
#or changed to this IMG_SIZE x IMG_SIZE
IMG_SIZE = 70

datadir = "animalsEN"

# categories = ["dog", "horse", "elephant", "butterfly", "chicken", "cat", 
# "cow", "sheep", "spider", "squirrel"]

categories = ["dog", "horse", "elephant", "cat", "squirrel"]

training_data = []

os.chdir("data")


def create_training_data():
    #Go through each folder
    for category in categories:
    #Gets us in the path for any of the folders for categories
    
        path = os.path.join(datadir, category)
        print(path)
        class_num = categories.index(category)
        #Iterate thru images
        #count = 0
        print("Current category:" + category)
        for img in os.listdir(path):

            #convert images with imread
            #convert images to gray scale b/c rgb data is 3x the size of grayscale, and don't need color differentiation
            #for classifying different animals, in this case, maybe for reptiles,etc
            #count+=1
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
            except Exception as e:
                pass
        #print(count)
            #use matplot to show the stuff
            #plt.imshow(img_array, cmap="gray")
            #plt.show()
            #break

create_training_data()

print("Length of training data: " + str(len(training_data)))


random.shuffle(training_data)

#for sample in training_data[:10]:
    #print(sample[1])

#features
X = []

#label
y = []

for features, label in training_data:
    X.append(features)
    y.append(label)
 
#-1 means that is catches all features, 1 is for gray scale
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close()

pickle_in = open("X.pickle", "rb")

X = pickle.load(pickle_in)