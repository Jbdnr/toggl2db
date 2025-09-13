"""Module to import data from Toggl API into the local database."""
import os
from dateutil import parser
from .api import TogglAPI
from .database import get_db_session
from .models import Project, TimeEntry

def prepare_dict(raw_dict, datetime_fields=None, array_fields=None):
    """
    Generic helper to normalize a raw dict from Toggl API.
    - Parses datetime fields using parser.isoparse
    - Normalizes array fields (comma-separated strings -> lists)
    """
    d = raw_dict.copy()

    # Parse datetime fields
    if datetime_fields:
        for field in datetime_fields:
            if field in d:
                dt_str = d.get(field)
                d[field] = parser.isoparse(dt_str) if dt_str else None

    # Normalize array fields
    if array_fields:
        for field in array_fields:
            val = d.get(field)
            if val is None:
                d[field] = None
            elif isinstance(val, str):
                d[field] = val.split(',')
            elif isinstance(val, list):
                d[field] = val
            else:
                d[field] = None

    return d


def prepare_project_dict(raw_dict):
    """Prepare and convert raw project dictionary from Toggl API."""
    return prepare_dict(raw_dict, datetime_fields=[
        'at', 'created_at', 'server_deleted_at', 'rate_last_updated', 'start_date'
    ])


def prepare_time_entry_dict(raw_dict):
    """Prepare and convert raw time entry dictionary from Toggl API."""
    return prepare_dict(raw_dict,
                        datetime_fields=['start', 'stop', 'at', 'server_deleted_at'],
                        array_fields=['tags', 'tag_ids'])


def import_toggl_data(start_date_str, end_date_str):
    """Import data from Toggl API and store it in the local database."""
    api = TogglAPI("https://api.track.toggl.com/api/v9", api_key=os.getenv('TOGGL_API_KEY'))
    time_entries = api.get_time_entries(start_date=start_date_str, end_date=end_date_str)
    projects = api.get_projects()
    api.close()

    project_objects = [Project(**prepare_project_dict(p)) for p in projects]
    te_objects = [TimeEntry(**prepare_time_entry_dict(te)) for te in time_entries]

    with get_db_session() as session:
        for obj in project_objects:
            session.merge(obj)
        for obj in te_objects:
            session.merge(obj)
