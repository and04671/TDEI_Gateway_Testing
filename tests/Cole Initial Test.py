import requests
import json
from dotenv import load_dotenv
import os
from utilities import *

load_dotenv()
USERNAME = os.getenv('TDEI_un')
PASSWORD = os.getenv('TDEI_pw')

base_url = "https://tdei-gateway-stage.azurewebsites.net"

def authenticate2(username, password):
    url = base_url + '/api/v1/authenticate'
    credentials = {'username': username, 'password': password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(credentials), headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    #print("response: ", response.json())
    return response.json()['access_token']

def list_project_groups(access_token, page_no=1, page_size=50):
    url = base_url + "/api/v1/project-group"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'page_no': page_no, 'page_size': page_size}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    # Write the response to a JSON file
    with open('project_groups.json', 'w') as outfile:
        json.dump(response.json(), outfile)
    return response.json()


token = authenticate2(USERNAME, PASSWORD)
project_groups = list_project_groups(token)