import requests
import logging
from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)

class EmeraldApiClient:
    """A client for the Emerald API."""

    def __init__(self, email, password):
        """Initialize the client."""
        self._email = email
        self._password = password
        self._token = None
        self._token_expiry = datetime.now()

    def login(self):
        """Login to the Emerald API and get a token."""
        url = "https://api.emerald-ems.com.au/api/v1/customer/sign-in"
        payload = {
            "app_version": "1.2.1",
            "device_name": "Xiaomi MIX Alpha",
            "device_os_version": "12",
            "device_token": "",
            "device_type": "android",
            "email": self._email,
            "passcode": None,
            "password": self._password,
        }
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "ok",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            self._token = response.json().get("token")
            self._token_expiry = datetime.now() + timedelta(hours=23)
            return True
        return False

    def refresh_token(self):
        """Refresh the API token."""
        url = "https://api.emerald-ems.com.au/api/v1/customer/token-refresh"
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "ok",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
        }
        payload = {
            "app_version": "1.2.1",
            "device_name": "Xiaomi MIX Alpha",
            "device_os_version": "12",
            "device_type": "android",
            "background_sync_count": 0,
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            self._token = response.json().get("token")
            self._token_expiry = datetime.now() + timedelta(hours=23)
            return True
        return False

    def _ensure_token(self):
        """Ensure the token is valid."""
        if self._token is None or datetime.now() >= self._token_expiry:
            if not self.login():
                _LOGGER.error("Failed to login to Emerald API")
                return False
        return True

    def get_properties(self):
        """Get the list of properties."""
        if not self._ensure_token():
            return None
        
        url = "https://api.emerald-ems.com.au/api/v1/customer/property/list"
        headers = {"Authorization": f"Bearer {self._token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_energy_data(self, device_id, start_date, end_date):
        """Get energy data for a device."""
        if not self._ensure_token():
            return None

        url = "https://api.emerald-ems.com.au/api/v1/customer/device/get-by-date/flashes-data"
        headers = {"Authorization": f"Bearer {self._token}"}
        params = {
            "device_id": device_id,
            "start_date": start_date,
            "end_date": end_date,
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return None
