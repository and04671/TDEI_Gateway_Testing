import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import zipfile
import json
import tempfile
import pandas as pd
import zipfile
import shutil

# Load environment variables from .env file
load_dotenv()

# Constants
BASE_URL = "https://tdei-gateway-stage.azurewebsites.net"
AUTH_ENDPOINT = "/api/v1/authenticate"
GTFS_FLEX_ENDPOINT = "/api/v1/gtfs-flex"

# Credentials
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Function to authenticate and get token
def authenticate(username, password):
    url = BASE_URL + AUTH_ENDPOINT
    credentials = {'username': username, 'password': password}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(credentials), headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    #print("response: ", response.json())
    return response.json()['access_token']

# Function to upload GTFS Flex file
def upload_gtfs_flex(access_token, file_path, metadata):
    url = BASE_URL + GTFS_FLEX_ENDPOINT
    headers = {
        'Authorization': f'Bearer {access_token}',
        }
    
    # Convert metadata to JSON string
    metadata_json = json.dumps(metadata)
    # Prepare the files for the request
    with open(file_path, 'rb') as file:
        files = {
            'meta': (None, metadata_json, 'application/json'),
            'file': (os.path.basename(file_path), file, 'application/octet-stream')
        }
        
        response = requests.post(url, headers=headers, files=files)

        response.raise_for_status()
        return response.json()

# Function to get available API versions
def get_api_versions(access_token):
    url = BASE_URL + "/api/v1/api"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to get the status of an uploaded record
def get_status(access_token, tdeiRecordId):
    url = BASE_URL + "/api/v1/status"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'tdeiRecordId': tdeiRecordId}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Function to list project groups
def list_project_groups(access_token, page_no=1, page_size=50):
    url = BASE_URL + "/api/v1/project-group"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'page_no': page_no, 'page_size': page_size}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    # Write the response to a JSON file
    with open('project_groups.json', 'w') as outfile:
        json.dump(response.json(), outfile)
    return response.json()

def get_current_utc_time():
    """
    Returns the current UTC time in the specified format.
    
    Returns:
    str: A string representing the current UTC time in YYYY-MM-DDTHH:MMZ format.
    """
    # Get current UTC time
    current_utc_time = datetime.utcnow()

    # Return the current time in the specified format
    return current_utc_time.strftime("%Y-%m-%dT%H:%MZ")

def get_valid_from():
    """
    Returns the current date and time in ISO 8601 format with UTC 'Z' suffix.
    """
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ")

def get_valid_to(days=30):
    """
    Returns the date and time 30 days from now in ISO 8601 format with UTC 'Z' suffix.

    Args:
    days (int): Number of days to add to the current date. Default is 30.
    """
    future_date = datetime.utcnow() + timedelta(days=days)
    return future_date.strftime("%Y-%m-%dT%H:%MZ")

def list_project_groups(access_token, page_no=1, page_size=50):
    url = BASE_URL + "/api/v1/project-group"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'page_no': page_no, 'page_size': page_size}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    with open('project_groups.json', 'w') as outfile:
        json.dump(response.json(), outfile)
    return response.json()

def list_gtfs_flex_services(access_token, project_group_id=None, page_no=1, page_size=10):
    url = 'https://tdei-gateway-stage.azurewebsites.net/api/v1/gtfs-flex/services'
    headers = {'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
    params = {
        'page_no': page_no,
        'page_size': page_size
    }
    if project_group_id:
        params['tdei_project_group_id'] = project_group_id

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

    return response.json()  # Return the parsed JSON response

def unzip_and_rezip(directory):
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            # Construct full file path
            file_path = os.path.join(directory, filename)
            
            # Unzip the file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Extract all the contents into the same directory
                zip_ref.extractall(directory)

            # Re-zip the contents (this assumes the zip contains a folder with the same name as the zip file)
            folder_name = os.path.splitext(filename)[0]
            folder_path = os.path.join(directory, folder_name)
            with zipfile.ZipFile(file_path, 'w') as zip_ref:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        # Create a relative path for each file to keep the directory structure
                        relative_path = os.path.relpath(os.path.join(root, file), directory)
                        zip_ref.write(os.path.join(root, file), relative_path)

def clean_and_unzip(directory):
    # Delete everything but .zip files
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and not filename.endswith('.zip'):
            os.remove(file_path)
        elif os.path.isdir(file_path) and not filename.endswith('.zip'):
            shutil.rmtree(file_path)

    # Unzip files into folders
    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            zip_path = os.path.join(directory, filename)
            extract_folder = os.path.splitext(zip_path)[0]
            os.makedirs(extract_folder, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)

    # Rezip folders into .zip files
    for filename in os.listdir(directory):
        folder_path = os.path.join(directory, filename)
        if os.path.isdir(folder_path):
            zip_path = folder_path + '.zip'
            with zipfile.ZipFile(zip_path, 'w') as zip_ref:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Adding file to zip
                        zip_ref.write(file_path, os.path.relpath(file_path, folder_path))



def match_and_combine_project_ids(csv_file_path, output_csv_path, access_token):
    project_groups = list_project_groups(access_token)
    df = pd.read_csv(csv_file_path)

    # Prepare a list to store the new rows
    new_rows = []

    for _, row in df.iterrows():
        project_name = row['Project Name']
        for project in project_groups:
            if project['project_group_name'] == project_name:
                # Get the services for the project group
                services = list_gtfs_flex_services(access_token, project['tdei_project_group_id'])
                if services:
                    first_service_id = services[0]['tdei_service_id']  # Assuming the service ID is in the first element
                else:
                    first_service_id = ''

                new_row = {
                    'project_id': project['tdei_project_group_id'],
                    'service_id': first_service_id,
                    'filename': row.get('file', '')
                }
                new_rows.append(new_row)
                break

    # Convert the list of dictionaries to a DataFrame
    new_df = pd.DataFrame(new_rows)

    # Save the new DataFrame to a CSV file
    new_df.to_csv(output_csv_path, index=False)
    print(f"New CSV file created successfully at {output_csv_path}.")


def process_gtfs_flex_files(directory):
    try:
        '''
        # Usage
        directory = 'gtfs_flex_zip_files'
        clean_and_unzip(directory)
        
        # Usage
        directory = 'gtfs_flex_zip_files'
        clean_and_unzip(directory)
        '''
        token = authenticate(USERNAME, PASSWORD)
        print("Authentication successful. Token GTFS:", token)
        #print("API Versions GTFS:", get_api_versions(token))
        #print("Project Groups GTFS:", list_project_groups(token))

        valid_from = get_valid_from()
        valid_to = get_valid_to()
        project_id = ''
        service_id = ''
        
        # Read the CSV file into a DataFrame
        csv_df = pd.read_csv('./matched_project_ids.csv')

        # Loop through all zip files in the directory
        for filename in os.listdir(directory):
            #print("zip filename: ", filename)
            if filename.endswith('.zip'):
                #print("filename: ", filename)
                zip_path = os.path.join(directory, filename)
                # Find matching project and service IDs from CSV
                matched_row = csv_df[csv_df['filename'] == filename]
                if not matched_row.empty:
                    project_id = matched_row.iloc[0]['project_id']
                    service_id = matched_row.iloc[0]['service_id']
                    #print("project_id: ", project_id)
                    #print("service_id: ", service_id)
                    
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # Extract to a temporary directory
                    with tempfile.TemporaryDirectory() as temp_dir:
                        zip_ref.extractall(temp_dir)
                        
                        # Search for a JSON file and parse it
                        for file in os.listdir(temp_dir):
                            #print("file: ", file)
                            if file.endswith('.geojson'):
                                json_path = os.path.join(temp_dir, file)
                                #print("json_path: ", json_path)
                                with open(json_path, 'r') as json_file:
                                    data = json.load(json_file)
                                    #print("data: ", data)
                                    
                                    # Check if the data is a FeatureCollection
                                    if data.get("type") == "FeatureCollection":
                                        # Keep only the first feature in the FeatureCollection
                                        if len(data["features"]) > 0:
                                            data["features"] = [data["features"][0]]
                                            
                                    polygon = data

                                    gtfs_flex_metadata = {
                                        'tdei_project_group_id': project_id,
                                        'tdei_service_id': service_id,
                                        'collected_by': 'Anat Caspian',
                                        'collection_date': get_current_utc_time(),
                                        'collection_method': 'manual',
                                        'valid_from': valid_from,
                                        'valid_to': valid_to,
                                        'data_source': 'InHouse',
                                        'polygon': polygon,
                                        'flex_schema_version': 'v2.0'
                                    }
                                    
                                    # Check if service_id is empty
                                    if service_id != '' and project_id != '':
                                        #print("gtfs_flex_metadata: ", gtfs_flex_metadata)
                                        
                                        #print("zip_path: ", zip_path)
                                        output_directory = "output"
                                        # Get filename without file extension 
                                        # Get only the file name without the directory path and file extension
                                        filenamenoext = os.path.splitext(os.path.basename(zip_path))[0]

                                        print("filenamenoext: ", filenamenoext)
                                        
                                        output_file_path = os.path.join(output_directory, filenamenoext + '.json')
                                        # Write gtfs_flex_metadata to a JSON file
                                        with open(output_file_path, 'w') as outfile:
                                            json.dump(gtfs_flex_metadata, outfile)
                                            
                                        response = upload_gtfs_flex(token, zip_path, gtfs_flex_metadata)
                                        print("GTFS Flex file uploaded successfully. Response:", response)
                   
    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", err)


# Main script
if __name__ == "__main__":
    token = authenticate(USERNAME, PASSWORD)
    #print("token: ", token)
    csv_file_path = './Staging Upload Dataset - GTFS-Flex.csv'
    output_csv_path = './matched_project_ids.csv'

    # Call the function with your CSV file paths and access token
    #match_and_combine_project_ids(csv_file_path, output_csv_path, token)

    try:
        process_gtfs_flex_files('./gtfs_flex_zip_files')
    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", err)
