# SI507-project
SI507 final project.
The main program to create plotly dash is final project

This is a plotly dashboard showing the pollution in each state in the U.S. It also shows relevant tweets in recent days.
## Get the tokens

### Mapbox tokens
Get free Mapbox tokens at https://docs.mapbox.com/help/getting-started/access-tokens/. 

Then fill the token in the line
  
    px.set_mapbox_access_token("<Your access token>")
### Twitter API
Get free Twitter API for developers at https://developer.twitter.com/en/docs/twitter-api.

Replace the variables `API_Key`, `API_Key_Secret`, `Bearer_Token`, `Access_Token`, `Access_Token_Secret` with the keys in your account.

### US EPA Air quality data API
Get free API key with email at https://aqs.epa.gov/aqsweb/documents/data_api.html#signup.

Replace with your email and key in `email`, `aqi_key`.

## How to interact with the dashboard
### Left sidebar
You can choose the pollutant name (radio button) to see the pollution map of each type. There are total 6 choices, the default choice is PM2.5.

There is also a dropdown to choose the state, and a date selection bar. The default value is Michigan on 01/01/2020. The range is from 01/01/2015 to 12/31/2021.

After selection, you will be able to see the pollution map of a certain type of pollutant of a state on one day.

### Right sidebar
You can choose the number of tweets you'd like to see by the dropdown box. (5, 10, 20)

The default number is 10.

## Required python packages
The required python packages are:
<ul>
  <li>requests</li>
  <li>numpy</li>
  <li>us</li>
  <li>datetime</li>
  <li>pandas</li>
  <li>statistics</li>
  <li>jupyter_dash</li>
  <li>dash</li>
  <li>dash_bootstrap_components</li>
</ul>

## Data Structure
The data strcutures of air pollution data and tweets data are both trees, and they are connected by state.
The us library is used to translate FIPS code to state name (and vice versa).

The air data contains latitude and longitude of each site, then it is divided into air pollution index like SO2, CO, etc., and air quality index (AQI).

The tweet data contains number of tweets, and a list of tweet capture results. Within the result, there are tweet id, text and its public metrics.

`construct.py` is used to create trees from json file. The `air_cache.json` and `tweet_cache.json` files are the cache files containing a small portion of data. 
The construction python file will read from these them, and create trees to `StateNews` and `Site` classes. `Site` class refers to air pollution data structure, while `StateNews` refers to tweet data structure.

`StateNews` stores all the required tweets of a state in it. The `Tweet` class represents a single tweet.

Also, a `.ipynb` version is provided to each python file.
