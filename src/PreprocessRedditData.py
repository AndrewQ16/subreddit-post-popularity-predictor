import os
import csv
import cv2
import tensorflow as tf
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import pickle
import sys

''' 
    If time allows it, integrate time of post into predicting the final outcome
'''
os.chdir("data")

# Find the maximum length of any caption in our dataset
def calc_max_length(tensor):
    return max(len(t) for t in tensor)

# Count the amount of non-spaced characters   
def wordsCount(string):


    counter = 0
    flag = False
    for c in string:
        if c != ' ' and flag == False:
            flag = True
        
        if c == ' ' and flag == True:
            flag = False
            counter+=1
    
    if string[len(string) - 1 ] != ' ':
        counter+=1
    return counter


def format_data():
    # tokenize text and then put it in a pickle file
    # put the images into a pickle file
    # Choose the top 5000 words from the vocabulary
    captions = []
    img_data = []
    scores = []
    max_caption_length = 0

    IMG_SIZE = int(sys.argv[1])

    with open("UpdatedData.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        
        for row in csvreader:
            full_img_path = os.path.abspath(os.curdir) + "/RedditImages/" + row[1] + '.jpg'
            if(os.path.exists(full_img_path) == False):
                continue
            img_path = None
            img_array = None
            new_array = None
            try:
                img_path = "RedditImages/" + row[1] + ".jpg"
                img_array = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
            except:
                print("Failed to transform img: {}".format(row[1]))
                continue

            caption = '<start> ' + row[0] + ' <end>'
            captions.append(caption)
            img_data.append(new_array)
            scores.append(row[5])

            max_caption_length = max(max_caption_length, wordsCount(caption))
            
            
            
    # at this point you have the captions and images in lists
    # shuffle the data sets
    train_captions, train_img_data, training_scores = shuffle(
        captions,img_data,scores, random_state=1)

    # take the top 5000 used words
    top_k = 5000
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=top_k, 
                                                    oov_token="<unk>",
                                                    filters='!"#$%&()*+.,-/:;=?@[\]^_`{|}~ ' )
    
    tokenizer.fit_on_texts(train_captions)

    tokenizer.word_index['<pad>'] = 0
    tokenizer.index_word[0] = '<pad>'

    # Create the tokenized vectors
    train_seqs = tokenizer.texts_to_sequences(train_captions)
    
    # Pad each vector to the max_length of the captions
    # If you do not provide a max_length value, pad_sequences calculates it automatically
    cap_vector = tf.keras.preprocessing.sequence.pad_sequences(train_seqs,maxlen=max_caption_length ,padding='post')

    print(cap_vector[:5])


    train_img_data = np.array(train_img_data).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    train_captions = np.array(cap_vector)
    
    pickle_out = open("reddit_images-{}.pickle".format(IMG_SIZE), "wb")
    pickle.dump(img_data, pickle_out)

    pickle_out = open("reddit_captions.pickle", "wb")
    pickle.dump(train_captions, pickle_out)

    pickle_out = open("reddit_scores.pickle", "wb")
    pickle.dump(training_scores, pickle_out)


if __name__ == "__main__":
    format_data()
    pass