import os
import praw
import prawcore
import re
import csv
import datetime
import emoji


def fixData():
    # open RedditData.csv
    os.chdir("data")
    needIdList = []
    reddit = praw.Reddit(client_id= 'SEo8q0S8iGyYpw',
                         client_secret='xDvwrr2KS5oZoo51BdJCMUdFg2I',
                         user_agent='aww_data_scrape')
    i = 0
    with open("DataPart1.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            i+=1
            if len(row) == 6:
                # find it's id:
            
                redditorName = row[1]
            
                if "i.redd" not in row[2]:
                    continue

                try:
                    submissions = reddit.redditor(redditorName).submissions.top('all')
                
                    for submission in submissions:
                        if submission.title == row[0]:
                            temp = [row[0], submission.id, row[1],row[2],"T",submission.score, row[5]]
                            needIdList.append(temp)
                            break

                except (prawcore.exceptions.NotFound, prawcore.exceptions.Forbidden) as e:
                    print("Error at row {}".format(i))
                    continue

                

            else:
                # add to list
                needIdList.append(row)

    # write to UpdatedData.csv
    with open("UpdatedData.csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(needIdList)


    


if __name__ == "__main__":
    fixData()
    pass