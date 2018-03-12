'''
Created on Jan 29, 2018
@author: ethanrussett
'''
import praw
from praw.models.reddit.more import MoreComments
import json
from operator import sub

def reddit_find(player):

    the_subreddits = ['MLBdraft','collegebaseball','baseball','OnTheFarm','InternationalBaseball']
    reddit = praw.Reddit(client_id = 'erFABv7J5pYtPg' , client_secret = '_2m3UJoSMhF7QPVHMtfNNf5c5gU', ussername = 'ethanrussett' ,password = 'baseball26', user_agent= 'datascrape')
    
    fields = ['selftext','title', 'subreddit_name_prefix','downs','name','ups','domain','created','selftext_html','subreddit_id','url','permalink']
    
    feildscom = ['body','downs','ups','permalink']
    
    key_word1 = player
    players_dic = {}
    finaldic = {}
    b=0
    def organize_comments(submission):            
        submission.comments.replace_more(limit=10) #Hits the more comment button
        all_com = {}
        a =0
        for comment in submission.comments.list():
            comdict = {}
            for k in range(len(feildscom)):
                for key in vars(comment):
                    if key == feildscom[k] and k != (len(feildscom)-1):
                        comdict.update({feildscom[k]:vars(comment)[key]})
                    elif key == feildscom[k] and k == (len(feildscom)-1):
                        comdict.update({feildscom[k]:'https://www.reddit.com'+ vars(comment)[key]})
            all_com.update({str(a):comdict})
            a=a+1
        return all_com
    
    def organize_submission(submission):
        sub = vars(submission)
        subdict = {}
        for k in range(len(fields)):
                for key in sub:
                    if key == fields[k] and k != (len(fields)-1):
                        subdict.update({fields[k]:sub[key]})
                    elif key == fields[k] and k == (len(fields)-1):
                        subdict.update({fields[k]:'https://www.reddit.com'+ sub[key]})
        return subdict
                    
    
    def dic_to_json(scram_dic, fields):
        dic = {}
        for key in scram_dic:
            if key in fields:
                dic[key] = scram_dic[key]
        players_dic.update(dic)
        return players_dic

    for i in range(len(the_subreddits)):
        
        subreddit = reddit.subreddit(the_subreddits[i])
        new_subreddit = subreddit.new(limit= 1000) #The number of posts that are scanned in a single subreddit
        for submission in new_subreddit:
            if key_word1 in submission.title or key_word1 in submission.selftext:
                org_submission = organize_submission(submission) 
                org_com = organize_comments(submission)
                finaldic.update({str(b):{'submission':org_submission, 'comments':org_com}})
                b=b+1
               
    '''                          
                                
                   
            for comment in submission.comments.list():
                if key_word1 in comment.body:
                    com = (vars(comment)) #Adds the comment with keyword to list
                    players_dic = dic_to_json(com,fields)
                elif len(comment.replies) > 0:
                    for reply in comment.replies:
                        if key_word1 in reply.body:
                            rep = (vars(reply)) #Adds Reply with keyword to list 
                            players_dic = dic_to_json(rep,fields)
    '''
    
    return finaldic

    