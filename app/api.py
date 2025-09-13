"""Simple wrapper for Toggl API using requests library."""
import logging
import requests

logging.basicConfig(level=logging.INFO)

class TogglAPI:
    """Simple wrapper for Toggl API."""

    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        # xxxx:api_token format (xxxx indicating user's personal token)
        self.session.auth = (api_key, 'api_token')

        if api_key:
            self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method, endpoint, **kwargs):
        """
        Internal method to send an HTTP request.

        kwargs can include: params, data, json, headers, etc.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method=method, url=url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("An error occurred: %s", e)
            return None

    def get_time_entries(self, start_date=None, end_date=None):
        """Get time entries for a given date range."""
        params={'start_date': start_date, 'end_date': end_date}
        return self._request('GET', '/me/time_entries', params=params)

    def get_projects(self):
        """Get all projects."""
        return self._request('GET', '/me/projects')

    def close(self):
        """Close the API session."""
        self.session.close()
        logging.info("API session closed.")
