#  -*- coding: utf-8 -*-
import tweepy
import sys
import json
from tweepy import OAuthHandler
import time
import re
global uid
global ids
global totaluid
global numu

consumer_key = 'jqJ14ABXYg2OMxLeYj34oNjba'
consumer_secret = '80l4LY3yfwfMhHPdKY9lw7lxOjHNxABX5SwEMHbSNvTG2ECFFj'
access_token = '3698906844-MKIzH5CiDmnrSNc1roiT1WIELMS9JJWKDhHmPA1'
access_secret = '9d9gW5onDbQAIo1GscKxFlLjDPC7BruX4oT6RqcY9lvU0'

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

api = tweepy.API(auth)

def limit_handled(cursor):
    numm = 0
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            numm += 1
            print("pull rest")
            print("pull timmer counter:"+str(numm))
            time.sleep(60)
            print("pull resume")
        except tweepy.error.TweepError:
            yield []
            return             

def cashe(uid):
    txtname = ("ids"+str(uid)+".txt")
    try:
        file_object2 = open(txtname,'r')
        b = []
        lines = file_object2.readlines()
        for a in lines:
            line = re.sub("[\n''' ]", '', a)
            b.append(line)
        file_object2.close()
        return b
    except:
        return False

    
def follower_page(uid):
    ids = cashe(uid)
    if ids != False:
        	print("cashe")
        	return ids
    elif ids == False:
        print("noncashe")
        ids = []
        for page in limit_handled(tweepy.Cursor(api.followers_ids,user_id=uid).pages()):
            ids.extend(page)
        txtname = str("ids"+str(uid)+".txt")
        with open(txtname,"a") as f:
            for i in ids:
                k=' '.join([str(i)])
                f.write(k+"\n")
        return ids
        

def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        try:
            initializer = next(it)
        except StopIteration:
            raise TypeError('reduce() of empty sequence with no initial value')
    accum_value = initializer
    for x in it:
        accum_value = function(accum_value, x)
    return accum_value
    
print("Begin reading standard base")
uid =  "498084894"
numu = 0
totaluid = []
file_object2 = open("total.txt",'r')
b = []
lines = file_object2.readlines()
for a in lines:
        line = re.sub("[\n''' ]", '', a)
        b.append(line)
file_object2.close()
totaluid = b
print("Finish reading base, the number of base now is "+str(len(totaluid)))


def isfurry(uid,totaluid):
    numif = 0
    isf = cashe(uid)
    if isf != False:
        print("Cashed")
    elif isf == False:
        print("Noncashed")
        isf = []
        for page in limit_handled(tweepy.Cursor(api.friends_ids,user_id=uid).pages()):
            isf.extend(page)
        print("Following "+str(len(isf)))
    for i in isf:
        if i in totaluid:
            numif +=1
    print(str(numif)+" in common for following")
    print("Percentage of total following"+str(numif/(len(isf)+0.00000001)))
    a = numif/(len(isf)+0.00001)
    i = str(str(uid)+"\n"+str(len(isf))+"\n"+str(a)+"\n")
    with open("record2.txt","a") as f:
        f.write(i)
    if numif == 0 or len(isf) == 0:
        print("BiJiao following False and 0")
        return False
    elif numif/(len(isf)+0.00000001) <= 0.3:
        print("BiJiao following False")
        return False
    else:
        print("BiJiao True")
        return True
	

def totaluser(ids,numu,totaluid):
    for i in ids:
        totaluid.append(i)
    totaluid = quchong(totaluid)
    return totaluid,totaluid[numu]

def totaluserfalse(numu,totaluid):
        return totaluid[numu]
    
    

def quchong(totaluid):
    func = lambda x,y:x if y in x else x + [y]
    totaluid = reduce(func, [[], ] + totaluid)
    return totaluid
    

def bijiao(uid,ids,totaluid):
    numc = 0
    for i in ids:
        if i in totaluid:
            numc +=1
    print(str(numc)+" in common.")
    print("Percentage of common is "+str(numc/(len(ids)+0.00001)))
    i = str(uid)+"\n"+str(numc)+"\n"+str(numc/(len(ids)+0.00001))+"\n"
    with open("record.txt","a") as f:
        f.write(i)
    if numc == 0 or len(ids) == 0:
        print("BiJiao False and 0 numbers found")
        return False
    elif numc/(len(ids)+0.00001) <= 0.01 or numc <= 5:
        print("BiJiao False")
        return False
    else:
        print("BiJiao True")
        return True
	

def main(uid,numu,totaluid):
    numu = 0
    while numu < len(totaluid):
        print("This is the "+str(numu+1)+" time(s) running.")
        ids = follower_page(uid)
        print("The currently number of followers of "+ str(uid) + " is " +str(len(ids)) )
        totaluid = quchong(totaluid)
        print("The current base amount is "+str(len(totaluid)))
        result = bijiao(uid,ids,totaluid)
        print("Result is "+str(result))
        if result == True:
            totaluid,uid = totaluser(ids,numu,totaluid)
            print("The new uid is "+str(uid))
            with open("total.txt","w") as f:
                if len(ids) > 0:
                    for i in totaluid:
                        k=' '.join(str(i))
                        f.write(k+"\n")
            print("Finish")
            numu +=1
            result = True
        if result == False:
            result = isfurry(uid,totaluid)
            if result == True:
                print(str(uid)+'is furry.')
                totaluid,uid = totaluser(ids,numu,totaluid)
                print("The new uid is "+str(uid))
                print("len of ids is "+str(len(ids)))
                if len(ids) > 0:
                    with open("total.txt","w") as f:
                        for i in totaluid:
                            k=' '.join(str(i))
                            f.write(k+"\n")
                        print("Finish")
                numu +=1
                result = True
            else:
                    print(str(uid)+"is not a furry.")
                    totaluid.remove(uid)
                    uid = totaluserfalse(numu,totaluid)
                    with open("total.txt","w") as f:
                        for i in totaluid:
                            k=' '.join(str(i))
                            f.write(k+"\n")
                        print("Finish")
                    numu +=1
                    result = True
    print("finish")
    with open("totallen.txt","w") as f:
        i = len(totaluid)
        k=' '.join(str(i))
        f.write(k+"\n")
        print("finish")

main(uid,numu,totaluid)
    


