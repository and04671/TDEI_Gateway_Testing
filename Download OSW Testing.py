import os
import requests
import json
from dotenv import load_dotenv
import requests, zipfile, io

load_dotenv()
USERNAME = os.getenv('stagepoc_user')
PASSWORD = os.getenv('stagepoc_user_pw')
KEY = os.getenv('stagepoc_user_key')

base_url = "https://tdei-gateway-stage.azurewebsites.net"


def authenticate(username, password):
    url = base_url + "/api/v1/authenticate"
    credentials = {'username': username, 'password': password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(credentials), headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    #print("response: ", response.json())
    return response.json()['access_token']

def download_osw_files(access_token):
    headers = {
        'accept': 'application/octet-stream',
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        'format': 'osw',
    }

    response = requests.get(
        'https://tdei-gateway-stage.azurewebsites.net/api/v1/osw/d95444192f954a178b2b443e30732eba',
        params=params,
        headers=headers,
    )

    with open('dataset.zip', 'wb') as f:
        f.write(response.content)

#x = authenticate(USERNAME,PASSWORD)
#download_osw_files(x)



def list_osw_versions(apiKey):
    url = base_url + "/api/v1/osw/versions"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'x-api-key': apiKey
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

list_osw_versions(KEY)

