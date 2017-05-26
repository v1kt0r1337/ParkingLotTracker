#Python 2.7.6
#RestfulClient.py

#GET

import requests
from requests.auth import HTTPDigestAuth
import json



# Replace with the correct URL
url = "http://158.37.63.8/api/v0/parkinglots"

# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
r = requests.get(url)
#print (myResponse.status_code)

# For successful API call, response code will be 200 (OK)
if(r.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(r.content)

    print(jData)
else:
  # If response code is not ok (200), print the resulting http error code with description
    r.raise_for_status()