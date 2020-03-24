'''
Collect data from r/aww and places the information into a CSV file

'''
import os
import praw
import re
import csv
import datetime
import emoji

'''
Grab the top 1000 new posts in r/aww
'''
def grabRedditPosts():
    reddit = praw.Reddit(client_id= 'SEo8q0S8iGyYpw',
                         client_secret='xDvwrr2KS5oZoo51BdJCMUdFg2I',
                         user_agent='aww_data_scrape')

    posts = reddit.subreddit('aww').new(limit=1000)

    # print("Printing new post links:")
    # for post in posts:
    #     print('Post: ' + post.title + '\n url: ' + post.url + 
    #     '\n date: ' + str(get_date(post)) + '\n upvote score: ' + str(post.score) + '\n')

    return posts

'''
Check if newly grabbed posts are in the CSV file
'''
def addPosts():
    posts = grabRedditPosts()
    rowsToAppend = []
    

    os.chdir("data")
    for post in posts:
        with open("RedditData.csv", 'r') as csvfile:

            if emoji.emoji_count(post.title) > 0:
                continue


            csvreader = csv.reader(csvfile)
            isInCsv = False

            # Check that we only deal with images
            if "i.redd" not in post.url:
                    continue

            #do a scan to see which of the posts aren't in this file yet
            for row in csvreader:
                # "2" is the index in which the url is located


                if post.url + " " == row[2]:
                    isInCsv = True
                    break         

                
            if isInCsv == False:   
                rowsToAppend.append([post.title, post.author ,post.url + ' ', "F", 0, get_date(post)])
            
    print("Added in: {} new rows".format(len(rowsToAppend)))
                
    with open("RedditData.csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rowsToAppend)
        

def get_date(submission):
    date = submission.created
    return datetime.datetime.fromtimestamp(date)


'''
Run the script
'''
def main():
    addPosts()
    

if __name__ == "__main__":
    main()