# Project TDEI Staging API Integration

This document provides guidelines on setting up and testing the utility functions and validation pipeline used for interacting with the TDEI staging instance API.

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Setup

1. **Create and activate a virtual environment (optional but recommended):**

   For Windows:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   For macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install the required packages:**

   Install `pytest`, `requests`, `requests-mock`, and `httpx` to run the tests, mock HTTP requests, and support asynchronous HTTP calls, respectively:

   ```bash
   pip install pytest requests requests-mock httpx
   ```

## Project Structure

```
your_project/
├── tests/
│   ├── test_utilities.py  # Your test file
├── utilities.py           # File containing utility functions to test
├── README.md              # This README file
└── .env                   # Environment variables (if used)
```

## Use of each file and directory

Here's a brief explanation of each file and directory in the given list:

- `.env`: A file used to store environment variables, like API keys or database connection strings, that you don't want to hard-code into your source files.
- `README.md`: A markdown file containing information about the project, such as an overview, setup instructions, and usage details.
- `TDEI Gateway Stage API.postman_collection.json`: A Postman collection file containing pre-configured API requests for the TDEI Gateway Stage API, useful for testing and interacting with the API outside of code.
- `TDEI-gtfs-csv-validator`: A directory (possibly containing a project or tool) for validating GTFS CSV files against the GTFS specifications or custom rules.
- `TDEI-internaldocs`: A directory that likely contains internal documentation for the TDEI project.
- `TDEI-python-lib-osw-validation`: A directory that likely contains a Python library project for validating OSW (Open Street Walk) data.
- `TDEI-python-osw-validation`: A directory containing a Python project or scripts for OSW data validation.
- `pipelines.py`: A Python file that likely contains code defining data processing or validation pipelines, perhaps for the workflow illustrated in the API interactions.
- `test_utilities.py`: A Python file containing test cases for the utility functions defined in `utilities.py`, likely using a framework like pytest.
- `utilities.py`: A Python file containing utility functions, they interact with the TDEI Gateway API, as described earlier.
  
## Writing Tests

- Place your test cases in `test_utilities.py`.
- Use `requests_mock` to mock HTTP responses.
- Use `pytest` and `httpx` for asynchronous test cases.

## Running Tests

1. **Navigate to your project directory:**

   ```bash
   cd path/to/your_project
   ```

2. **Run the pytest tests:**

   Execute all tests in the `tests` directory:

   ```bash
   pytest tests
   ```

   To run a specific test file:

   ```bash
   pytest tests/test_utilities.py
   ```

3. **Review the test output:**

   - Pytest will display the results of each test, indicating whether they passed or failed.
   - For failed tests, pytest provides detailed output, showing what went wrong.

## Uploading to Fusion Database

To upload to the fusion database, use the following command (replace placeholders with actual values):

```bash
ogr2ogr -f "PostgreSQL" PG:"host=tdei.postgres.database.azure.com dbname=forBill user= password=" wa.microsoft.graph.nodes.OSW.geojson -nln osw_data -lco GEOMETRY_NAME=polygon -lco FID=tdei_record_id
```

Based on the provided premise and focusing on Python usage for interacting with the staging instance, here's how each section can be elaborated in the `README.md`:

---

## Environment Setup

Before interacting with the staging API, ensure your environment is correctly set up:

```markdown
Create a `.env` file in the root of your project directory and add your configuration variables. For example:
```

```python
API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
STAGING_BASE_URL=https://tdei-staging-api-url.com
```

Use the `python-dotenv` package to load these variables in your Python script:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv('API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
STAGING_BASE_URL = os.getenv('STAGING_BASE_URL')
```


## API Endpoint Configuration

Set up and use the API endpoint within your Python application:

```markdown
Configure the `base_url` in your `utilities.py` or similar file to point to the staging API:
```

```python
# In utilities.py
base_url = STAGING_BASE_URL  # Loaded from environment variables

async def get_api_endpoint(endpoint):
    return f"{base_url}/{endpoint}"
```

## Authentication and Authorization

Handle authentication and manage authorization tokens effectively:

```markdown
Implement functions to authenticate and refresh tokens as needed:
```

```python
import requests

async def authenticate():
    auth_url = get_api_endpoint('api/v1/authenticate')
    credentials = {'username': 'your_username', 'password': 'your_password'}
    response = requests.post(auth_url, json=credentials)
    return response.json()['token']

async def refresh_token(api_key):
    refresh_url = get_api_endpoint('api/v1/refresh-token')
    headers = {'x-api-key': api_key}
    response = requests.post(refresh_url, headers=headers)
    return response.json()['new_token']
```

```

## Detailed API Functionality

Provide examples and explanations for API interactions:

```markdown
For each utility function, give clear examples of API usage. For instance:
```

```python
async def list_pathways(api_key, bbox):
    url = get_api_endpoint('api/v1/pathways')
    headers = {'x-api-key': api_key}
    params = {'bbox': bbox}
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

## Error Handling and Debugging

Outline strategies for managing errors and debugging API interactions:

```markdown
Use try-except blocks to handle possible API errors gracefully:
```

```python
async def safe_api_call():
    try:
        response = list_pathways(API_KEY, 'bbox_values')
        response.raise_for_status()  # Will raise an exception for 4xx/5xx errors
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
```

## Best Practices

Discuss best practices for API consumption:

```markdown
Implement rate limiting and retries in your API calls to handle load and transient failures:
```

```python
import backoff

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
async def robust_api_call():
    return safe_api_call()
```


## Change Management

Describe how to keep up with changes to the API:

```markdown
Regularly check the API documentation or subscribe to the API's change log to stay informed about updates. Implement version control in your API interactions to manage changes effectively:
```

```python
API_VERSION = 'v1'

async def get_api_endpoint(endpoint):
    return f"{base_url}/{API_VERSION}/{endpoint}"
```