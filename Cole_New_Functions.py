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

#how does that differ from this method?
async def authenticate2(username, password, apiKey):

    url = base_url + "/api/v1/authenticate"

    payload = json.dumps({
    "username": "<string>",
    "password": "<string>"})

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'}

    response = requests.request("POST", url, headers=headers, data=payload)

#this function takes the access token and returns all project groups
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

#this function should upload a new osw data for pre-release
async def upload_osw_dataset(
        apiKey,
        dataset_id,
        metadata,
        changeset,
        bearerToken
):
    url = base_url + "/api/v1/osw/upload/<string>/<string>?derived_from_dataset_id={{dataset_id}}"

    payload = {
        'dataset': '<string>',
        'metadata': '<string>',
        'changeset': '<string>'
    }

    files = []

    headers = {
        'Content-Type': 'multipart/form-data',
        'Accept': 'application/text',
        'Authorization': 'Bearer {{bearerToken}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

