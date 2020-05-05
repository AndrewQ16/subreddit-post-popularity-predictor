import os
import urllib.request
import csv


'''
This script is just to go to the link of each image and download it

'''

def dl_img():
    #full_path = file_path _ file_name + '.jpg'
    os.chdir("data")
    with open("UpdatedData.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        #skip the first row which just contains column names
        next(csvreader, None)
        i = 0
        for row in csvreader:
            i+=1
        
            full_path = os.path.abspath(os.curdir) + "/RedditImages/" + row[1] + '.jpg'
            
            if os.path.exists(full_path):
                continue

            try:
                urllib.request.urlretrieve(row[3], full_path)
                
            except:
                print("Error for row: {}".format(i)) 
                
                continue


dl_img()