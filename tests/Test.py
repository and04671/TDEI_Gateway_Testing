import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
USERNAME = os.getenv('TDEIusername')
PASSWORD = os.getenv('TDEIpassword')

base_url = "https://tdei-gateway-stage.azurewebsites.net"

def authenticate(username, password):
    url = base_url + "/api/v1/authenticate"
    payload = json.dumps({ "username": username, "password": password})
   # print(payload)
    headers = { 'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': '{{apiKey}}' }
    response = requests.request("POST", url, headers=headers, data=payload)

def authenticate(username, password):
    url = "https://tdei-gateway-stage.azurewebsites.net/api/v1/authenticate"
    credentials = {'username': username, 'password': password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(credentials), headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    print("response: ", response.json())
    #return response.json()['access_token']

#authenticate('', '')