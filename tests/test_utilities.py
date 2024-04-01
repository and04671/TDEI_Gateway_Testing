import pytest
import requests_mock
from utilities import *
import asyncio


#Cole: starting completely from scratch here. What is a fixture?
@pytest.fixture
async def api_key():
    """
    Fixture to provide a static API key for testing purposes.
    """
    return "test_api_key"

@pytest.fixture
async def bearer_token():
    """
    Fixture to provide a static bearer token for testing purposes.
    """
    return "test_bearer_token"

@pytest.fixture
async def dataset_id():
    """
    Fixture to provide a static dataset ID for testing purposes.
    """
    return "test_dataset_id"

@pytest.fixture
async def api_base_url():
    """
    Fixture to provide the base URL of the API for testing purposes.
    """
    return "https://tdei-gateway-stage.azurewebsites.net"

async def test_refresh_token(requests_mock, api_key, api_base_url):
    """
    Tests the refresh token functionality by mocking a POST request to the refresh-token API endpoint.
    """
    test_response = {"access_token": "new_access_token", "expires_in": 3600, "refresh_token": "new_refresh_token"}
    requests_mock.post(f"{api_base_url}/api/v1/refresh-token", json=test_response)
    # Call the refresh_token function here, assuming it's defined in your utilities
    await refresh_token(api_key)
    assert requests_mock.last_request.json() == "<expected_payload_here>"
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_authenticate(requests_mock, api_key, api_base_url):
    """
    Tests the authentication process by mocking a POST request to the authenticate API endpoint.
    """
    test_response = {"access_token": "auth_token", "expires_in": 3600, "refresh_token": "refresh_token"}
    requests_mock.post(f"{api_base_url}/api/v1/authenticate", json=test_response)
    # Call the authenticate function here, assuming it's defined in your utilities
    await authenticate("test_user", "test_pass", api_key)
    assert requests_mock.last_request.json() == {"username": "test_user", "password": "test_pass"}
    assert requests_mock.last_request.headers["x-api-key"] == api_key


# Example for upload_osw_dataset
async def test_upload_osw_dataset(requests_mock, api_key, bearer_token, dataset_id, api_base_url):
    """
    Tests the OSW dataset upload functionality by mocking a POST request to the OSW upload API endpoint.
    """
    test_response = {"tdei_record_id": "new_record_id"}
    requests_mock.post(f"{api_base_url}/api/v1/osw/upload/{dataset_id}", json=test_response)
    # Call the upload_osw_dataset function here, assuming it's defined in your utilities
    await upload_osw_dataset(api_key, dataset_id, "<file_path>", "<metadata_path>", "<changeset_path>", bearer_token)
    # Here, you should check the request body, headers, and other relevant details
    assert requests_mock.last_request.headers["Authorization"] == f"Bearer {bearer_token}"


async def test_authenticate(requests_mock, api_key, api_base_url):
    """
    Tests the authentication process by mocking a POST request to the authenticate API endpoint.
    """
    test_response = {"token": "auth_token"}
    requests_mock.post(f"{api_base_url}/api/v1/authenticate", json=test_response)
    await authenticate("test_user", "test_pass", api_key)
    assert requests_mock.last_request.json() == {"username": "test_user", "password": "test_pass"}
    assert requests_mock.last_request.headers["x-api-key"] == api_key


async def test_get_upload_status(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests the OSW dataset upload functionality by mocking a POST request to the OSW upload API endpoint.
    """
    test_response = {"status": "uploaded"}
    requests_mock.get(f"{api_base_url}/api/v1/osw/upload/status/{tdei_record_id}", json=test_response)
    await get_upload_status(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key


async def test_publish_osw_dataset(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests the functionality to publish an OSW dataset by mocking a POST request to the publish API endpoint.
    """

    test_response = {"status": "published"}
    requests_mock.post(f"{api_base_url}/api/v1/osw/publish/{tdei_record_id}", json=test_response)
    await publish_osw_dataset(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_get_publish_status(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests retrieval of the publish status for a dataset by mocking a GET request to the publish status API endpoint.
    """
    test_response = {"status": "publish_in_progress"}
    requests_mock.get(f"{api_base_url}/api/v1/osw/publish/status/{tdei_record_id}", json=test_response)
    await get_publish_status(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key


async def test_validate_osw_dataset(requests_mock, api_key, dataset, bearer_token, api_base_url):
    """
    Tests the validation process for an OSW dataset by mocking a POST request to the validate API endpoint.
    """
    test_response = {"status": "validation_started"}
    requests_mock.post(f"{api_base_url}/api/v1/osw/validate", json=test_response)
    await validate_osw_dataset(api_key, dataset, bearer_token)
    assert requests_mock.last_request.headers["Authorization"] == f"Bearer {bearer_token}"

async def test_get_validation_status(requests_mock, api_key, job_id, api_base_url):
    """
    Tests retrieval of the validation status for a job by mocking a GET request to the validation status API endpoint.
    """
    test_response = {"status": "validation_complete"}
    requests_mock.get(f"{api_base_url}/api/v1/osw/validate/status/{job_id}", json=test_response)
    await get_validation_status(api_key, job_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key


async def test_reformat_osw_dataset(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests the reformatting process for an OSW dataset by mocking a POST request to the convert API endpoint.
    """

    test_response = {"status": "reformatting_started"}
    requests_mock.post(f"{api_base_url}/api/v1/osw/convert/{tdei_record_id}", json=test_response)
    await reformat_osw_dataset(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_list_osw_versions(requests_mock, api_key, api_base_url):
    """
    Tests listing of available OSW dataset versions by mocking a GET request to the versions API endpoint.
    """
    test_response = ["version1", "version2"]
    requests_mock.get(f"{api_base_url}/api/v1/osw/versions", json=test_response)
    await list_osw_versions(api_key)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_download_osw_files(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests downloading of OSW files by mocking a GET request to the download API endpoint.
    """
    test_response = b"binary data"
    requests_mock.get(f"{api_base_url}/api/v1/osw/{tdei_record_id}/files", content=test_response)
    await download_osw_files(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_invalidate_osw_record(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests the invalidation of an OSW record by mocking a DELETE request to the OSW API endpoint.
    """
    test_response = "OSW record invalidated"
    requests_mock.delete(f"{api_base_url}/api/v1/osw/{tdei_record_id}", text=test_response)
    await invalidate_osw_record(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_flatten_osw_dataset(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests the flattening process for an OSW dataset by mocking a POST request to the dataset-flatten API endpoint.
    """
    test_response = "Dataset flattening initiated"
    requests_mock.post(f"{api_base_url}/api/v1/osw/dataset-flatten/{tdei_record_id}", json=test_response)
    await flatten_osw_dataset(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_get_flattening_status(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests retrieval of the flattening status for a dataset by mocking a GET request to the dataset-flatten status API endpoint.
    """
    test_response = {"status": "flattening_in_progress"}
    requests_mock.get(f"{api_base_url}/api/v1/osw/dataset-flatten/status/{tdei_record_id}", json=test_response)
    await get_flattening_status(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_get_dataset_bounding_box_status(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests retrieval of the bounding box status for a dataset by mocking a GET request to the dataset-bbox status API endpoint.
    """
    test_response = {"status": "bounding_box_ready"}
    requests_mock.get(f"{api_base_url}/api/v1/osw/dataset-bbox/status/{tdei_record_id}", json=test_response)
    await get_dataset_bounding_box_status(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_download_dataset_file(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests downloading of a dataset file by mocking a GET request to the dataset-bbox download API endpoint.
    """
    test_response = b"binary data of the dataset"
    requests_mock.get(f"{api_base_url}/api/v1/osw/dataset-bbox/download/{tdei_record_id}", content=test_response)
    await download_dataset_file(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_get_dataset_bounding_box(requests_mock, api_key, tdei_record_id, api_base_url, bearer_token):
    """
    Tests retrieval of the dataset bounding box by mocking a POST request to the dataset-bbox API endpoint.
    """
    test_response = "Bounding box data"
    requests_mock.post(f"{api_base_url}/api/v1/osw/dataset-bbox/{tdei_record_id}", json=test_response)
    await get_dataset_bounding_box(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["Authorization"] == f"Bearer {bearer_token}"

async def test_list_osw_files(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests the listing of OSW files for a specific record by mocking a GET request to the OSW files API endpoint.
    """
    test_response = ["file1", "file2"]
    requests_mock.get(f"{api_base_url}/api/v1/osw/{tdei_record_id}/files", json=test_response)
    await list_osw_files(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key
async def test_get_gtfs_pathways_file(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests the retrieval of a specific GTFS pathways file by mocking a GET request to the GTFS pathways file API endpoint.
    """
    test_response = b"GTFS pathways file data"
    requests_mock.get(f"{api_base_url}/api/v1/gtfs-pathways/{tdei_record_id}", content=test_response)
    await get_gtfs_pathways_file(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_list_gtfs_pathways_versions(requests_mock, api_key, api_base_url):
    """
    Tests listing of GTFS pathways versions by mocking a GET request to the GTFS pathways versions API endpoint.
    """
    test_response = ["v1", "v2"]
    requests_mock.get(f"{api_base_url}/api/v1/gtfs-pathways/versions", json=test_response)
    await list_gtfs_pathways_versions(api_key)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_list_stations(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests the listing of stations for a specific GTFS pathways record by mocking a GET request to the GTFS pathways stations API endpoint.
    """
    test_response = ["station1", "station2"]
    requests_mock.get(f"{api_base_url}/api/v1/gtfs-pathways/{tdei_record_id}/stations", json=test_response)
    await list_stations(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_list_pathways_files(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests the listing of pathways files for a specific GTFS pathways record by mocking a GET request to the GTFS pathways files API endpoint.
    """
    test_response = ["pathway1", "pathway2"]
    requests_mock.get(f"{api_base_url}/api/v1/gtfs-pathways/{tdei_record_id}/files", json=test_response)
    await list_pathways_files(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_create_pathways_file(requests_mock, api_key, tdei_record_id, bearer_token, api_base_url):
    """
    Tests the creation of a pathways file for a specific GTFS pathways record by mocking a POST request to the GTFS pathways API endpoint.
    """
    test_response = "Pathways file created"
    requests_mock.post(f"{api_base_url}/api/v1/gtfs-pathways/{tdei_record_id}", text=test_response)
    await create_pathways_file(api_key, tdei_record_id, bearer_token)
    assert requests_mock.last_request.headers["Authorization"] == f"Bearer {bearer_token}"

async def test_get_gtfs_flex_file(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests the retrieval of a specific GTFS flex file by mocking a GET request to the GTFS flex file API endpoint.
    """
    test_response = b"GTFS flex file data"
    requests_mock.get(f"{api_base_url}/api/v1/gtfs-flex/{tdei_record_id}", content=test_response)
    await get_gtfs_flex_file(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_list_gtfs_flex_versions(requests_mock, api_key, api_base_url):
    """
    Tests the listing of GTFS flex versions by mocking a GET request to the GTFS flex versions API endpoint.
    """
    test_response = ["flex1", "flex2"]
    requests_mock.get(f"{api_base_url}/api/v1/gtfs-flex/versions", json=test_response)
    await list_gtfs_flex_versions(api_key)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_list_flex_files(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests the listing of flex files for a specific GTFS flex record by mocking a GET request to the GTFS flex files API endpoint.
    """
    test_response = ["flex_file1", "flex_file2"]
    requests_mock.get(f"{api_base_url}/api/v1/gtfs-flex/{tdei_record_id}/files", json=test_response)
    await list_flex_files(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_upload_gtfs_flex_file(requests_mock, api_key, tdei_record_id, bearer_token, api_base_url):
    """
    Tests the upload of a GTFS flex file for a specific record by mocking a POST request to the GTFS flex upload API endpoint.
    """
    test_response = "GTFS flex file uploaded"
    requests_mock.post(f"{api_base_url}/api/v1/gtfs-flex/{tdei_record_id}", text=test_response)
    await upload_gtfs_flex_file(api_key, tdei_record_id, bearer_token)
    assert requests_mock.last_request.headers["Authorization"] == f"Bearer {bearer_token}"

async def test_list_services(requests_mock, api_key, api_base_url):
    """
    Tests the listing of services by mocking a GET request to the services API endpoint.
    """
    test_response = ["service1", "service2"]
    requests_mock.get(f"{api_base_url}/api/v1/services", json=test_response)
    await list_services(api_key)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_list_project_groups(requests_mock, api_key, api_base_url):
    """
    Tests the listing of project groups by mocking a GET request to the project groups API endpoint.
    """
    test_response = ["project_group1", "project_group2"]
    requests_mock.get(f"{api_base_url}/api/v1/project-groups", json=test_response)
    await list_project_groups(api_key)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_list_api_versions(requests_mock, api_key, api_base_url):
    """
    Tests the listing of API versions by mocking a GET request to the API versions endpoint.
    """
    test_response = ["api_version1", "api_version2"]
    requests_mock.get(f"{api_base_url}/api/v1/api-versions", json=test_response)
    await list_api_versions(api_key)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_get_status(requests_mock, api_key, api_base_url):
    """
    Tests the retrieval of the general status of the system by mocking a GET request to the status API endpoint.
    """
    test_response = {"status": "operational"}
    requests_mock.get(f"{api_base_url}/api/v1/status", json=test_response)
    await get_status(api_key)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_initiate_confidence_calculation(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests initiating the confidence calculation for a dataset by mocking a POST request to the confidence calculation API endpoint.
    """
    test_response = "Confidence calculation initiated"
    requests_mock.post(f"{api_base_url}/api/v1/confidence/calculate/{tdei_record_id}", json=test_response)
    await initiate_confidence_calculation(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_get_confidence_status(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests retrieving the status of the confidence calculation for a dataset by mocking a GET request to the confidence status API endpoint.
    """
    test_response = {"status": "confidence_calculation_complete"}
    requests_mock.get(f"{api_base_url}/api/v1/confidence/status/{tdei_record_id}", json=test_response)
    await get_confidence_status(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_download_converted_file(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests downloading a converted file for a dataset by mocking a GET request to the download API endpoint for converted files.
    """
    test_response = b"converted file data"
    requests_mock.get(f"{api_base_url}/api/v1/osw/convert/download/{tdei_record_id}", content=test_response)
    await download_converted_file(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_get_format_status(requests_mock, api_key, tdei_record_id, api_base_url):
    """
    Tests checking the status of the format conversion process for a dataset by mocking a GET request to the format status API endpoint.
    """
    test_response = {"status": "formatting_complete"}
    requests_mock.get(f"{api_base_url}/api/v1/osw/convert/status/{tdei_record_id}", json=test_response)
    await get_format_status(api_key, tdei_record_id)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

async def test_get_dataset_bounding_box(requests_mock, api_key, api_base_url, bearer_token):
    """
    Tests retrieval of the dataset bounding box by mocking a POST request to the dataset-bbox API endpoint.
    """
    test_response = "Dataset bounding box details"
    job_id = "test_job_id"
    bbox = [1.0, 2.0, 3.0, 4.0]
    requests_mock.post(f"{api_base_url}/api/v1/osw/dataset-bbox?tdei_record_id={job_id}&bbox={bbox[0]}&bbox={bbox[1]}&bbox={bbox[2]}&bbox={bbox[3]}", text=test_response)
    await get_dataset_bounding_box(api_key, job_id, bbox)
    assert requests_mock.last_request.headers["Authorization"] == f"Bearer {bearer_token}"
    assert requests_mock.last_request.json() == {"bbox": bbox}

async def test_list_gtfs_pathways_versions(requests_mock, api_key, api_base_url):
    """
    Tests the listing of GTFS pathways versions available by mocking a GET request to the GTFS pathways versions API endpoint.
    """
    test_response = ["version1", "version2"]
    requests_mock.get(f"{api_base_url}/api/v1/gtfs-pathways/versions", json=test_response)
    await list_gtfs_pathways_versions(api_key)
    assert requests_mock.last_request.headers["x-api-key"] == api_key

