#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import numpy as np
import os,re,us
import json
import plotly.express as px
px.set_mapbox_access_token("pk.eyJ1IjoiZmN4LWtpbGlnIiwiYSI6ImNsMHIwaG5rODJmY2QzYnM1NW1rcHRjOHMifQ.1kdhIW8dwvtyNDFHOCyx5g")
API_Key = 'pzFDw36S40GxhJLXmtLYN4MfW'
API_Key_Secret = 'bV7FUFPK4Eaqmts26r26POmC7JNlgyt7vSdR63QDEHSms8UL5J'
Bearer_Token = 'AAAAAAAAAAAAAAAAAAAAAKGFbQEAAAAAWcrusWRsy0QE3lLWsvF7lPbnJfc%3DyWDpEWxNK1yLhFsRjSe7c9v5HoGXqIcX88Qmr4QGRI38lfgn15'
Access_Token = '1506028898525450241-LqmCE8DmRY7KSMOJL0WXULWyr7iA8D'
Access_Token_Secret = 'IXeFTTYLsXhc6lCt5POk7dgtH4No42dvtA4ZeHPxSp7DO'


# In[2]:


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


# In[3]:


search_url = "https://api.twitter.com/2/tweets/search/recent"
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {Bearer_Token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# In[4]:


def get_pop(json):
    result=0
    for v in json['public_metrics'].values():
        result += v
    return result


# In[5]:


class Tweet:
    def __init__(self,json):
        self.id=json['id']
        self.text=json['text']
        self.popularity=get_pop(json)


# In[6]:


def getalltweets(fips,num):
    StateName=us.states.lookup(str(fips).zfill(2)).name
    query=f"{StateName} pollution"
    query_params={
        'query':query,
        'max_results':num,
        'tweet.fields':'public_metrics',
    }
    result=[]
    c=connect_to_endpoint(search_url,query_params)
    #print(c['data'])
    try:
        for items in c['data']:
            result.append(Tweet(items))
        return c['data'],result
    except:
        result.append('No data recently!')
        return {},result


# In[7]:


class StateNews:
    def __init__(self,fips,num):
        self.state=us.states.lookup(str(fips).zfill(2)).name
        self.json, self.tweet=getalltweets(fips,num)
        self.number=num


# In[8]:


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

def save_cache(filename,cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(filename,"w")
    fw.write(dumped_json_cache)
    fw.close() 


# In[9]:


base_url="https://aqs.epa.gov/data/api/dailyData/byState?email=mingyuli@umich.edu&key=greenkit68&param="
pollutant_para={'co':"42101",'so2':"42401",'no2':"42602",'ozone':"44201",'pm10':"81102",'pm25':"88101"}

def geturl(pollutant_name,fips,date):
    url=base_url+pollutant_para[pollutant_name]+"&bdate="+date+"&edate="+date+"&state="+str(fips).zfill(2)
    return url

def getjson(url):
    return requests.get(url).json()['Data']


# In[10]:


def save_pollutant_cache(date, fips, pollutant):
    have_captured = pollutant + str(fips).zfill(2) + str(date)
    dic = open_cache(sitefile)
    if (have_captured in dic.keys()): # have found data in cache json file
        #print("find!")
        return dic[have_captured]
    else:
        #print("create cache")
        url=geturl(pollutant,str(fips),str(date)) # get the url for that date
        jsondata=getjson(url)
        dic[have_captured]=jsondata
        save_cache(sitefile,dic)
        return jsondata


# In[11]:


import datetime
now = datetime.datetime.now()

def save_tweet_cache(fips, num):
    tweet_dict = open_cache(tweetfile)
    have_captured = str(fips)+str(now.day)+str(now.hour)
    if have_captured in tweet_dict.keys():
        return tweet_dict[have_captured]
    else:
        news=StateNews(fips, num)
        #print(news.tweet[1].text)
        tweet_dict[have_captured]=news.json
        save_cache(tweetfile,tweet_dict)
        return news.json


# In[12]:


us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 
             'Colorado', 'Connecticut', 'Washington DC', 'Delaware', 'Florida',
             'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
             'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
             'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
             'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
             'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 
             'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 
             'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 
             'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']


# In[13]:


import pandas as pd
def airToDf(date,pollutant,fips):
    # transfer json to dataframe and plot
    jsonlst = save_pollutant_cache(date,fips,pollutant)
    sitenum = len(jsonlst)
    d = np.zeros((sitenum,3))
    sitelst = []
    for json in jsonlst:
        sitelst.append(Site(json))
    for i in range(sitenum):
        d[i,0] = sitelst[i].latitude
        d[i,1] = sitelst[i].longitude
        d[i,2] = sitelst[i].concentration
    return pd.DataFrame(d, columns=['latitude','longitude','concentration'])


# In[14]:


import statistics
from jupyter_dash import JupyterDash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
app = JupyterDash(external_stylesheets=[dbc.themes.BOOTSTRAP])
from datetime import date


# In[15]:


SELECT_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "height": "100%",
    "padding": "1rem 1rem",
    "backgroundColor": "#ebebeb",
    'display': 'inline-block',
    "border":"1px #b5b5b5 solid",
}

TWEET_STYLE = {
    "maxHeight": "600px", 
    "overflow": "scroll"
}

TWEETBAR_STYLE = {
    "left": 0,
    "padding-top": "1rem",
    "padding-left": "1rem",
    "padding-right": "1rem",
    "height": "100%",
    "backgroundColor": "#ebebeb",
    'display': 'inline-block',
    "border":"1px #b5b5b5 solid",
}

selectbar = html.Div(
    [
        html.H3('Pollutant Name'),
        dcc.RadioItems(id = 'pollutant-radio',
                        options = [{'label':'PM2.5','value':'pm25'},
                                   {'label':'PM10','value':'pm10'},
                                   {'label':'CO', 'value':'co'},
                                   {'label':'SO2', 'value':'so2'},
                                   {'label':'NO2','value':'no2'},
                                   {'label':'Ozone', 'value':'ozone'}],
                        value = 'pm25',
                      labelStyle={'display': 'block'}),
        html.H3(['Select state:']),
        dcc.Dropdown(id='state-dropdown', 
                    options=us_states, 
                    value="Michigan"),
        html.H3(['Select date:']),
        dcc.DatePickerSingle(
            id='datepick',
            min_date_allowed=date(2015, 1, 1),
            max_date_allowed=date(2021, 12, 31),
            initial_visible_month=date(2020, 1, 1),
            date=date(2020, 1, 1)
        ),
    ],
    style = SELECT_STYLE
)


tweets = html.Div([
        html.H4(['Tweet number with highest popularity:']),
        dcc.Dropdown(id='tweet-dropdown', 
                    options=[10,15,20], 
                    value=10),
        dbc.ListGroup(id='tweet-list',style=TWEET_STYLE)
    ],
    style = TWEETBAR_STYLE
)

pollutionmap = html.Div(dcc.Graph(id = 'PollutionMap'))

page = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(selectbar),
                dbc.Col(pollutionmap),
                dbc.Col(tweets),
            ]
        )
    ]
)

app.layout = page
@app.callback(
    Output('PollutionMap', 'figure'),
    Input('state-dropdown','value'),
    Input('pollutant-radio', 'value'),
    Input('datepick', 'date'))

def update_figure(state, pollutant, startdate):
    date_object = date.fromisoformat(startdate)
    datestring = str(startdate).replace('-','')
    fips = int(us.states.lookup(state).fips)
    airdf = airToDf(datestring,pollutant,fips)
    fig = px.scatter_mapbox(airdf, lat="latitude", lon="longitude", size='concentration', color = 'concentration',
                        center={'lat':statistics.median(airdf['latitude']),'lon':statistics.median(airdf['longitude'])},
                      color_continuous_scale=px.colors.cyclical.IceFire, zoom=8,width=850, height=750)
    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5)
    )
    return fig

@app.callback(
    Output('tweet-list','children'),
    Input('tweet-dropdown','value'),
    Input('state-dropdown','value')
)

def update_tweetlist(num, state):
    fips = int(us.states.lookup(state).fips)
    tweet_json = save_tweet_cache(fips,num)
    all_tweets = StateNews(fips, num).tweet
    save_tweet_cache(fips, num)
    result = []
    for tweet in all_tweets:
        newitem = dbc.ListGroupItem([
            html.Div([
            html.P(tweet.text),
            html.P('\U0001F525'+'Popularity: '+str(tweet.popularity))])
        ])
        result.append(newitem)
    return result
## Deploy app -------------------------------------------------------------
del app.config._read_only["requests_pathname_prefix"]
app.run_server(debug=True)

