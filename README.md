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
