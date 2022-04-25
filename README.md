# SI507-project
SI507 final project.

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
  <li>requests
  <li>numpy
  <li>us
  <li>datetime
  <li>pandas
  <li>statistics
  <li>jupyter_dash
  <li>dash
  <li>dash_bootstrap_components
