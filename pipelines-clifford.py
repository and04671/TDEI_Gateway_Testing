import pytest
import requests_mock
from utilities import *
import asyncio
import httpx

# Setting up base variables for API interaction
base_url = "https://tdei-gateway-stage.azurewebsites.net"
apiKey = "your_api_key"
username = "your_username"
password = "your_password"
dataset_id = "your_dataset_id"
osw_file_path = "osw_file_path"
gtfs_flex_file_path = "gtfs_flex_file_path"
gtfs_pathways_file_path = "gtfs_pathways_file_path"

# Asynchronous function to authenticate user and get a token using HTTPX client
async def authenticate(username, password, apiKey):
    url = f"{base_url}/api/v1/authenticate"
    payload = json.dumps({
        "username": username,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': apiKey
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=payload)
        print(response.text)

# Asynchronous function to refresh authentication token using HTTPX client
async def refresh_token(apiKey):
    url = f"{base_url}/api/v1/refresh-token"
    payload = "<string>"  # Replace <string> with the actual data if needed
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': apiKey
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=payload)
        print(response.text)

# Asynchronous pipeline function to execute a series of API calls for validating datasets

async def run_validation_pipeline(apiKey, username, password, dataset_id, osw_file, gtfs_flex_file, gtfs_pathways_file):
    # Authenticate and refresh token
    await authenticate(username, password, apiKey)
    await refresh_token(apiKey)

    # OSW Workflow
    await upload_osw_dataset(apiKey, osw_file, "metadata", "changeset", "bearerToken")
    await get_upload_status(apiKey, dataset_id)
    await validate_osw_dataset(apiKey, dataset_id)
    await get_validation_status(apiKey, dataset_id)
    await publish_osw_dataset(apiKey, dataset_id)
    await get_publish_status(apiKey, dataset_id)
    await download_converted_file(apiKey, dataset_id)
    await get_format_status(apiKey, dataset_id)
    await list_osw_versions(apiKey)
    await download_osw_files(apiKey, dataset_id)
    await invalidate_osw_record(apiKey, dataset_id)
    await flatten_osw_dataset(apiKey, dataset_id)
    await get_flattening_status(apiKey, dataset_id)
    await get_dataset_bounding_box_status(apiKey, dataset_id)
    await download_dataset_file(apiKey, dataset_id)
    await list_osw_files(apiKey, dataset_id)
    await initiate_confidence_calculation(apiKey, "tdei_record_id")
    await get_confidence_status(apiKey)

    # GTFS Pathways Workflow
    await get_gtfs_pathways_file(apiKey, dataset_id)
    await list_gtfs_pathways_versions(apiKey, dataset_id)
    await list_stations(apiKey, dataset_id)
    await list_pathways_files(apiKey, dataset_id)
    await create_pathways_file(apiKey, gtfs_pathways_file)

    # GTFS Flex Workflow
    await get_gtfs_flex_file(apiKey, dataset_id)
    await list_gtfs_flex_versions(apiKey, dataset_id)
    await list_flex_files(apiKey, dataset_id)
    await upload_gtfs_flex_file(apiKey, gtfs_flex_file)
    await list_services(apiKey, dataset_id)
    await list_project_groups(apiKey, dataset_id)

    # General status checks
    await list_api_versions(apiKey)
    await get_status(apiKey, dataset_id)

# Run the async pipeline function
async def main():
    await run_validation_pipeline(
        apiKey,
        username,
        password,
        dataset_id,
        osw_file_path,
        gtfs_flex_file_path,
        gtfs_pathways_file_path
    )
    
# Execute the main async function using asyncio
asyncio.run(main())
