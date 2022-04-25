#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import numpy as np
import us
import json
import plotly.express as px
px.set_mapbox_access_token("pk.eyJ1IjoiZmN4LWtpbGlnIiwiYSI6ImNsMHIwaG5rODJmY2QzYnM1NW1rcHRjOHMifQ.1kdhIW8dwvtyNDFHOCyx5g")
API_Key = 'pzFDw36S40GxhJLXmtLYN4MfW'
API_Key_Secret = 'bV7FUFPK4Eaqmts26r26POmC7JNlgyt7vSdR63QDEHSms8UL5J'
Bearer_Token = 'AAAAAAAAAAAAAAAAAAAAAKGFbQEAAAAAWcrusWRsy0QE3lLWsvF7lPbnJfc%3DyWDpEWxNK1yLhFsRjSe7c9v5HoGXqIcX88Qmr4QGRI38lfgn15'
Access_Token = '1506028898525450241-LqmCE8DmRY7KSMOJL0WXULWyr7iA8D'
Access_Token_Secret = 'IXeFTTYLsXhc6lCt5POk7dgtH4No42dvtA4ZeHPxSp7DO'
base_url="https://aqs.epa.gov/data/api/dailyData/byState?email="
email = "mingyuli@umich.edu"
aqi_key = "greenkit68"


# In[17]:


def get_pop(json):
    result=0
    for v in json['public_metrics'].values():
        result += v
    return result

class Tweet:
    def __init__(self,json):
        self.id=json['id']
        self.text=json['text']
        self.popularity=get_pop(json)


# In[26]:


class StateNews:
    def __init__(self,keys,json):
        self.state=us.states.lookup(keys[0:2]).name
        self.tweet=getalltweets(json)


# In[19]:


def getalltweets(jsonlst):
    result = []
    for items in jsonlst:
        result.append(Tweet(items))
    return result


# In[4]:


def addpollutant(json):
    if (json['parameter_code']=="42401"):
        return ("SO2", abs(json['arithmetic_mean']))
    elif (json['parameter_code']=="42101"):
        return ("CO",abs(json['arithmetic_mean']))
    elif (json['parameter_code']=="42602"):
        return ('NO2',abs(json['arithmetic_mean']))
    elif (json['parameter_code']=="44201"):
        return ('Ozone',abs(json['arithmetic_mean']))
    elif (json['parameter_code']=="81102"):
        return ('PM10',abs(json['arithmetic_mean']))
    elif (json['parameter_code']=="88101"):
        return ('PM25',abs(json['arithmetic_mean']))

class Site:
    def __init__(self,json=None):
        self.statecode=json['state_code']
        self.latitude=json['latitude']
        self.longitude=json['longitude']
        self.airname, self.concentration=addpollutant(json)


# In[5]:


sitefile='air_cache.json'  # cache for air pollution data archived site
tweetfile='tweet_cache.json'  # cache for daily tweets capture
def open_cache(filename):
    try:
        cache_file = open(filename, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


# In[14]:


allSites = []
def save_pollutant():
    dic = open_cache(sitefile)
    for have_captured in dic.keys():
        jsonlst = dic[have_captured]
        for json in jsonlst:
            allSites.append(Site(json))
save_pollutant()


# In[29]:


import datetime
now = datetime.datetime.now()

allTweets = []
def save_tweet():
    tweet_dict = open_cache(tweetfile)
    for k in tweet_dict.keys():
        allTweets.append(StateNews(k,tweet_dict[k]))

