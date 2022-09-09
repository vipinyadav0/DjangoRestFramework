# This is a third party application and can be any thing like Android, Java or any application
# we want data from database using api

import requests
import json

URL = "http://127.0.0.1:8080/api/"

req = requests.get(url=URL)

data = req.json()

print(data)
