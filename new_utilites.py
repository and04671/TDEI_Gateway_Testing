#Cole: this script will contain working versions of the utilities.py file for the current API release

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv('TDEI_un')
PASSWORD = os.getenv('TDEI_pw')

base_url = "https://tdei-gateway-stage.azurewebsites.net"

#function authenticates credidentials and returns access token
def authenticate(username, password):
    authendpt = "/api/v1/authenticate"
    url = base_url + authendpt
    credentials = {'username': username, 'password': password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(credentials), headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    print("response: ", response.json())
    return response.json()['access_token']

#how does that differ from this method, which requires an API key   ?
def authenticate2(username, password):

    url = base_url + "/api/v1/authenticate"

    payload = json.dumps({
    "username": username,
    "password": password})

    headers = {
    'Content-Type': 'application/json',
    'accept': 'application/json'}

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['access_token']

#this function takes the access token and returns all project groups


def list_osw_versions(access_token):

    url = base_url + "/api/v1/osw/versions"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['versions']


x = authenticate2(USERNAME, PASSWORD)
print(x)
y = list_osw_versions(x)
print (y)
