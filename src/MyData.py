import os
import random
import pickle
import numpy as np
import matplotlib.pyplot as plt
import cv2


# translate = {"cane": "dog", "cavallo": "horse", "elefante": "elephant", "farfalla": "butterfly", 
#     "gallina": "chicken", "gatto": "cat", "mucca": "cow", "pecora": "sheep", 
#     "scoiattolo": "squirrel", "dog": "cane", "cavallo": "horse", "elephant" : "elefante", 
#     "butterfly": "farfalla", "chicken": "gallina", "cat": "gatto", "cow": "mucca", "spider": "ragno", 
#     "squirrel": "scoiattolo"}


#The size that images get set to. That means any images passed to the model must be of the same size
#or changed to this IMG_SIZE x IMG_SIZE
IMG_SIZE = 30

datadir = "animalsEN"

# categories = ["dog", "horse", "elephant", "butterfly", "chicken", "cat", 
# "cow", "sheep", "spider", "squirrel"]

#categories = ["dog", "horse", "elephant", "cat", "squirrel"]

categories = ["dog", "cat"]

training_data = []

os.chdir("data")

try:
    f = open("X.pickle")
    os.remove("X.pickle")
except IOError:
    print("X.pickle not found")
finally:
    f.close()

try:
    f = open("y.pickle")
    os.remove("y.pickle")
except IOError:
    print("y.pickle not found")
finally:
    f.close()

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
            try:
                #convert image to a np array on gray scale, so (size,size, 1) insead of (size,size,3) for RGB
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                #print(img_array.shape) ====> (sizeX, sizeY). No third column cuz it's just grayscale
                
                #Resize an image to the specified IMG_SIZE
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
                #print(training_data) ===> prints the list that contains a narray object
                #print(categories[class_num]) => correctly outputs the value
                
            except Exception as e:
                
                pass
        #print(count)
            #use matplot to show the stuff
            #plt.imshow(img_array, cmap="gray")
            #plt.show()
            #break

create_training_data()

print("Length of training data: " + str(len(training_data)))

#shuffle the data otherwise will be in order: dog, dog... ,cat, cat..... etc
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
y = np.array(y)

pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close()
