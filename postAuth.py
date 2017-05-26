#Python 2.7.6
#RestfulClient.py

#POST

import requests
from requests.auth import HTTPDigestAuth
import json


data = {'deviceId': 'api', 'password': 'passord'}

url = "http://158.37.63.8:3000/api/v0/auth"

r = requests.post(url, data=data)

jData = r.json()

# For successful API call, response code will be 200 (OK)
if(r.ok):
    token = jData.get('token')
    message = jData.get('message')
    print(message)

else:
  # If response code is not ok (200), print the resulting http error code with description
  message = jData.get('message')
  print(message)
