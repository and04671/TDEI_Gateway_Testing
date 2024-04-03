import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv('TDEI_un')
PASSWORD = os.getenv('TDEI_pw')

base_url = "https://tdei-gateway-stage.azurewebsites.net"

#Cole: These functions are from 'gtfs-flex-upload-clifford.py' and seem to be way to authenticate
def authenticate3(username, password):
    authendpt = "/api/v1/authenticate"
    url = base_url + authendpt
    credentials = {'username': username, 'password': password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(credentials), headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    print("response: ", response.json())
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




#Cole: These two are functions from the ReadMe. These would seem to work to get authorization
async def authenticate2():
    auth_url = get_api_endpoint('api/v1/authenticate')
    credentials = {'username': 'your_username', 'password': 'your_password'}
    response = requests.post(auth_url, json=credentials)
    return response.json()['token']

# Authenticates the user with the provided credentials and API key
# Cole: API key isn't a parameter required to get a token? Do some user accts have an API key to start with?
async def authenticate(username, password, apiKey):
    url = base_url + "/api/v1/authenticate"

    payload = json.dumps({
        "username": "<string>",
        "password": "<string>"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': '{{apiKey}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

# Refreshes the authentication token using the given API key
async def refresh_token(apikey):
    url = base_url + "/api/v1/refresh-token"

    payload = "<string>"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': '{{apiKey}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# OSW

# Uploads an OpenSidewalks (OSW) dataset pre-release with given parameters

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


# Retrieves the upload status of an OSW dataset using its dataset ID

async def get_upload_status(apiKey, dataset_id):
    url = base_url + "/api/v1/osw/upload/status/{{dataset_id}}"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# Publishes the specified OSW dataset to make it available for users

async def publish_osw_dataset(apiKey, dataset_id):
    url = base_url + "/api/v1/osw/publish/{{dataset_id}}"

    payload = {}
    headers = {
        'Accept': 'application/text',
        'x-api-key': '{{apiKey}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# Retrieves the publication status of an OSW dataset using its dataset ID

async def get_publish_status(apiKey, dataset_id):
    url = base_url + "/api/v1/osw/publish/status/{{dataset_id}}"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# Checks the validation status of an OSW dataset using its dataset ID

async def get_validation_status(apiKey, dataset_id):
    url = base_url + "/api/v1/osw/validate/status/{{dataset_id}}"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)