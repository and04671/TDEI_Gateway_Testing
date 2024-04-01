
base_url = "https://tdei-gateway-stage.azurewebsites.net"

import requests
from requests.auth import HTTPBasicAuth

# Making a get request
response = requests.get("https://tdei-gateway-stage.azurewebsites.net/api/v1/authenticate",
                        auth=HTTPBasicAuth('', ''))

# print request object
print(response)