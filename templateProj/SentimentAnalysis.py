import praw
import time
import datetime
import json
from textblob import TextBlob

def main(array_of_subreddits):
    reddit = praw.Reddit(client_id='YGvFNM2_0jk-QA',
                         client_secret="SNivnpSLutE4Yq_nmbaqHqm2i30", password='this4tin',
                         user_agent='USERAGENT', username='hungryeung')
    file_writer = open("static/data.json", 'w')
    file_writer.write("[")
    writeCounter = 0
    for subreddit in array_of_subreddits:
        sub = reddit.subreddit(subreddit)
        counter = 0
        data = {}
        data["key"] = subreddit
        data["values"] = []
        for post in sub.search('post match thread', sort = "new", limit=10):
            counter+=1
            time = int(post.created * 1000)
            post.comment_sort = 'top'
            comment_counter = 4
            polarity_score = 0
            total_score =0
            for comment in post.comments:
                if comment_counter <= 0:
                    break
                if not hasattr(comment, 'body'):
                    continue
                commentTextBlob = TextBlob(comment.body)
                polarity_score += ((commentTextBlob.sentiment.polarity)*comment.score)
                total_score+=comment.score
                comment_counter-=1
            polarity_score = polarity_score / total_score
            data["values"].append([time, polarity_score])
        with file_writer as outfile:
            json.dump(data, outfile)
        file_writer = open("static/data.json", 'a')
        if writeCounter < len(array_of_subreddits) - 1:
            file_writer.write(",")
    file_writer = open("static/data.json", 'a')
    file_writer.write("]")
    file_writer.close()
main(["Gunners","reddevils","chelseaFC","liverpoolFC","coys","MCFC"])