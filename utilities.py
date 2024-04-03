#Cole: these functions are obviously incomplete.
# Admin users require a bearer token vs. require an API key; functions need option to 'swap' those out
# Most functions don't call for a bearer token

import requests
import json

base_url = "https://tdei-gateway-stage.azurewebsites.net"

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

# Authenticates the user with the provided credentials and API key
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
    
    files=[]

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


# Initiates the validation process for the specified OSW dataset

async def validate_osw_dataset(apiKey, dataset_id):
    url = base_url + "/api/v1/osw/validate"

    payload = {'dataset': '{{dataset_id}}'}
    files=[

    ]
    headers = {
    'Content-Type': 'multipart/form-data',
    'Accept': 'application/text',
    'Authorization': 'Bearer {{bearerToken}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


# Create a fun# Fetches the status of a format conversion request for an OSW dataset
async def get_format_status(apiKey, dataset_id):

    url = base_url + "/api/v1/osw/convert/status/{{dataset_id}}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)



# Downloads the converted file of an OSW dataset

async def download_converted_file(apiKey, dataset):

    url = base_url + "/api/v1/osw/convert/download/{{dataset_id}}"

    payload = {}
    headers = {
    'Accept': 'application/octet-stream',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# Initiates reformatting of an OSW dataset on demand

async def reformat_osw_dataset(apiKey, filename):

    url = base_url + "/api/v1/osw/convert"

    payload = {'file': '{{filename}}',
    'source': 'osw',
    'target': 'osm'}
    files=[

    ]
    headers = {
    'Content-Type': 'multipart/form-data',
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


# Initiates confidence calculation for a specified dataset
    
async def initiate_confidence_calculation(apiKey, tdei_record_id):

    url = base_url + "/api/v1/osw/confidence/calculate"

    payload = json.dumps({
    "tdei_record_id": "{{tdei_record_id}}"
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# Retrieves the status of the confidence calculation for a specified dataset

async def get_confidence_status(apiKey, dataset_id):

    url = base_url + "/api/v1/osw/confidence/status/{{dataset_id}}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# Lists all available versions of the OSW data

async def list_osw_versions(apiKey):

    url = base_url + "/api/v1/osw/versions"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# Downloads the OSW files as a zip archive for the specified dataset
    
async def download_osw_files(apiKey, dataset):

    url = base_url + "/api/v1/osw/{{dataset_id}}?format=osw"

    payload = {}
    headers = {
    'Accept': 'application/octet-stream',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# Invalidates an OSW record in the dataset

async def invalidate_osw_record(apiKey, dataset_id):

    url = base_url + "/api/v1/osw/{{dataset_id}}"

    payload = {}
    headers = {
    'Accept': 'application/text',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(response.text)

# Flattens an OSW dataset, potentially overwriting existing data if specified

async def flatten_osw_dataset(apiKey, dataset, override):

    url = base_url + "/api/v1/osw/dataset-flattern/{{dataset_id}}?override={{override}}"

    payload = {}
    headers = {
    'Accept': 'application/text',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# Retrieves the status of a flattening request for an OSW dataset

async def get_flattening_status(apiKey, dataset_id):

    url = base_url + "/api/v1/osw/dataset-flattern/status/{{dataset_id}}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# Fetches the status of the bounding box request for a dataset
async def get_dataset_bounding_box_status(apiKey, dataset_id):

    url = base_url + "/api/v1/osw/dataset-bbox/status/{{dataset_id}}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)



# Downloads the file for a dataset

async def download_dataset_file(apiKey, dataset_id):

    url = base_url + "/api/v1/osw/dataset-bbox/download/{{dataset_id}}"

    payload = {}
    headers = {
    'Accept': 'application/octet-stream',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# Retrieves a subgraph within a given bounding box for a dataset
async def get_dataset_bounding_box(
        apiKey, 
        dataset_id, 
        tdei_record_id, 
        bbox1,
        bbox2,
        bbox3,
        bbox4
        ):
    
    url = base_url + "/api/v1/osw/dataset-bbox?tdei_record_id={{tdei_record_id}}&"
    + "bbox={{bbox1}}&bbox={{bbox2}}&bbox={{bbox3}}&bbox={{bbox4}}"

    payload = {}
    headers = {
    'Accept': 'application/text',
    'Authorization': 'Bearer {{bearerToken}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

# Lists the OSW files that meet specified criteria

async def list_osw_files(
        apiKey, 
        dataset, 
        bbox1,
        bbox2,
        bbox3,
        bbox4,
        name,
        version,
        data_source,
        collection_method,
        collected_by,
        derived_from_dataset_id,
        collection_date,
        confidence_level,
        status,
        osw_schema_version,
        tdei_project_group_id,
        valid_from,
        valid_to,
        tdei_record_id,
        page_no,
        page_size
        ): 
    
    url = base_url + "/api/v1/osw?bbox={{bbox1}}&"
    + "bbox={{bbox2}}&bbox={{bbox2}}&bbox={{bbox3}}&name={{name}}"
    + "&version={{version}}&data_source={{data_souce}}&collection_method={{collection_method}}&collected_by={{collected_by}}&"
    + "derived_from_dataset_id={{derived_from_dataset_id}}&collection_date={{collection_date}}&confidence_level={{confidence_level}}&"
    + "status={{status}}&osw_schema_version={{osw_schema_version}}&tdei_project_group_id={{tdei_project_group_id}}&valid_from={{valid_from}}&"
    + "valid_to={{valid_to}}&tdei_record_id={{tdei_record_id}}&page_no={{page_no}}&page_size={{page_size}}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# GTFS Pathways
    
# Retrieves a GTFS pathways file for the specified dataset

async def get_gtfs_pathways_file(apiKey, dataset_id):

    url = base_url + "/api/v1/gtfs-pathways/{{dataset_id}}"

    payload = {}
    headers = {
    'Accept': 'application/octet-stream',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# Lists available versions of GTFS pathways data

async def list_gtfs_pathways_versions(apiKey, dataset):

    url = base_url + "/api/v1/gtfs-pathways/versions"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# Lists stations based on criteria such as project group and pagination
    
async def list_stations(
        apiKey, 
        dataset,
        tdei_project_group_id,
        page_no,
        page_size
        ):
    
    url = base_url + "/api/v1/gtfs-pathways/stations?"
    + "tdei_project_group_id={{tdei_project_group_id}}&page_no={{page_no}}&page_size={{page_size}}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# Lists pathways files meeting specified criteria

async def list_pathways_files(
        apiKey, 
        dataset,
        bbox1,
        bbox2,
        bbox3,
        bbox4,
        tdei_station_id,
        pathways_schema_version,
        date_time,
        tdei_project_group_id,
        tdei_record_id,
        page_no,
        page_size
        ):
    
    url = base_url + "/api/v1/gtfs-pathways?"
    + "bbox={{bbox1}}&bbox={{bbox2}}&bbox={{box3}}&bbox={{bbox4}}&"
    + "tdei_station_id={{tdei_station_id}}&pathways_schema_version={{pathways_schema_version}}&"
    + "date_time={{date_time}}&tdei_project_group_id={{tdei_project_group_id}}&"
    + "tdei_record_id={{tdei_record_id}}&page_no={{page_no}}&page_size={{page_size}}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# Creates a pathways file with the specified parameters

async def create_pathways_file(
        apiKey, 
        dataset, 
        filename, 
        metadata_filename, 
        bearerToken
        ):
    
    url = base_url + "/api/v1/gtfs-pathways"

    payload = {'file': '<string>',
    'meta': '[object Object]'}
    files=[

    ]
    headers = {
    'Content-Type': 'multipart/form-data',
    'Accept': 'application/text',
    'Authorization': 'Bearer {{bearerToken}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

## GTFS Flex
    
# Retrieves a GTFS flex file for the specified dataset

async def get_gtfs_flex_file(apiKey, dataset_id):
    url = base_url + "/api/v1/gtfs-flex/{{dataset_id}}"

    payload = {}
    headers = {
    'Accept': 'application/octet-stream',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# Lists available versions of GTFS flex data

async def list_gtfs_flex_versions(apiKey, dataset):

    url = base_url + "/api/v1/gtfs-flex/versions"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# Lists flex files meeting specified criteria

async def list_flex_files(
        apiKey, 
        dataset,
        bbox1,
        bbox2,
        bbox3,
        bbox4,
        flex_schema_version,
        tdei_project_group_id,
        date_time,
        tdei_record_id,
        page_no,
        page_size
        ):

    url = base_url + "/api/v1/gtfs-flex?tdei_service_id={{tdei_service_id}}&"
    + "bbox={{bbox1}}>&bbox={{bbox2}}&bbox={{bbox3}}&bbox={{bbox4}}&"
    + "flex_schema_version={{flex_schema_version}}&tdei_project_group_id={{tdei_project_group_id}}&"
    + "date_time={{date_time}}&tdei_record_id={{tdei_record_id}}&page_no={{page_no}}&page_size={{page_size}}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# Uploads a new GTFS flex file for the specified dataset

async def upload_gtfs_flex_file(
        apiKey, 
        dataset, 
        metadata_filename, 
        filename
        ):
    
    url = base_url + "/api/v1/gtfs-flex"

    payload = {'file': '{{filename}}',
    'meta': '{{metadata_filename}}'}
    files=[]
    headers = {
    'Content-Type': 'multipart/form-data',
    'Accept': 'application/text',
    'Authorization': 'Bearer {{bearerToken}}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)


# Lists services based on criteria such as project group, service type, and pagination

async def list_services(
        apiKey, 
        dataset, 
        tdei_project_group_id,
        service_type,
        page_no,
        page_size
        ):
    url = base_url + "/api/v1/services?tdei_project_group_id={{tdei_project_group_id}}"
    + "&service_type={{service_type}}&page_no={{page_no}}&page_size={{page_size}}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# Lists project groups based on pagination and optional project group ID

async def list_project_groups(
        apiKey, 
        dataset,
        page_no,
        page_size,
        project_group_id
        ):
    
    url = base_url + "/api/v1/project-group?page_no={{page_no}}&page_size={{page_size}}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# Lists available API versions

async def list_api_versions(apiKey):
    url = base_url + "/api/v1/api"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

# Retrieves the status of a specified entity or process

async def get_status(apiKey, dataset, tdei_record_id):
    url = base_url + "/api/v1/status?tdeiRecordId={{tdei_record_id}}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'x-api-key': '{{apiKey}}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)