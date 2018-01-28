import praw
import time
import datetime
from textblob import TextBlob

def main(subreddit):
    reddit = praw.Reddit(client_id='YGvFNM2_0jk-QA',
                         client_secret="SNivnpSLutE4Yq_nmbaqHqm2i30", password='this4tin',
                         user_agent='USERAGENT', username='hungryeung')

    sub = reddit.subreddit(subreddit)
    counter = 0
    list =[]
    for post in sub.search('post match thread', sort = "new", limit=None):
        counter+=1
        time = post.created
        time_stamp = (datetime.datetime.fromtimestamp(time))
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
        tuple = (polarity_score, time, post.url)
        list.append(tuple)
        filename = open("/static/"+subreddit + ".csv","w")
        filename.write('date,polarity,url\n')
        for tuple in list:
            filename.write(str(tuple[0])+","+str(tuple[1])+ "," +str(tuple[2])+'\n')
        filename.close()


main("Gunners")
# main("reddevils")
# main("chelseaFC")
# main("liverpoolFC")
# main("coys")
# main("MCFC")