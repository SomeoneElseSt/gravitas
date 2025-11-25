"""Earth Engine client initialization."""

import json
import os

import ee


def initialize_earth_engine() -> dict[str, str] | None:
    """
    Initialize Earth Engine with appropriate credentials.

    Returns error dict if initialization fails, None if successful.
    """
    # Check if running with service account (production)
    service_account_email = os.getenv("GCP_SERVICE_ACCOUNT_EMAIL")
    service_account_key_path = os.getenv("GCP_SERVICE_ACCOUNT_KEY_PATH")
    service_account_key_json = os.getenv("GCP_SERVICE_ACCOUNT_KEY_JSON")

    if service_account_email and (service_account_key_path or service_account_key_json):
        try:
            # Production: Use service account
            if service_account_key_json:
                # Key provided as JSON string
                key_data = json.loads(service_account_key_json)
                credentials = ee.ServiceAccountCredentials(
                    service_account_email, key_data=json.dumps(key_data)
                )
            elif service_account_key_path:
                # Key provided as file path - read the file
                with open(service_account_key_path, 'r') as f:
                    key_data = json.load(f)

                # Debug: print what we're using
                print(f"DEBUG: Using service account: {service_account_email}")
                print(f"DEBUG: Project ID in key: {key_data.get('project_id')}")

                credentials = ee.ServiceAccountCredentials(
                    service_account_email, key_data=json.dumps(key_data)
                )
            else:
                return {"error": "No service account key provided", "detail": ""}

            # Initialize with credentials only (no project parameter needed)
            print("DEBUG: Initializing Earth Engine with service account")
            ee.Initialize(credentials)
            print("DEBUG: Earth Engine initialized successfully")
            return None

        except Exception as e:
            return {"error": "Failed to initialize Earth Engine", "detail": str(e)}

    # Local development: Use project-based authentication
    project_name = os.getenv("GCP_PROJECT_NAME", "gravitasuhisteveapi")

    try:
        ee.Initialize(project=project_name)
        return None
    except Exception as e:
        return {
            "error": "Failed to initialize Earth Engine",
            "detail": f"Authentication failed. Run 'earthengine authenticate' first. Error: {e}",
        }


def get_ee_instance():
    """
    Get initialized Earth Engine instance.

    Initializes EE if not already initialized.
    Returns (ee_module, error_dict).
    """
    # Always initialize to ensure we use the correct credentials
    # EE caches initialization, so this is safe to call multiple times
    error = initialize_earth_engine()
    if error:
        return None, error
    return ee, None
