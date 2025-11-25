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
            else:
                # Key provided as file path
                credentials = ee.ServiceAccountCredentials(
                    service_account_email, key_file=service_account_key_path
                )

            ee.Initialize(credentials)
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
    try:
        # Check if already initialized
        ee.Number(1).getInfo()
        return ee, None
    except Exception:
        # Not initialized, try to initialize
        error = initialize_earth_engine()
        if error:
            return None, error
        return ee, None
