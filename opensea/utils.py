from datetime import datetime, timezone


def export_file(content, file_name):
    """Creates a new file with the specified content and file name. If the file
    already exists, overwrites it.

    Args:
        content (str or bytes): Content to be inserted into the file.
        file_name (str): Name of the file to be created. Eg. 'export.json'.
    """
    with open(file_name, "wb") as f:
        f.write(content)


def str_to_datetime_utc(str):
    """Converts a string into UTC datetime object.

    Args:
        str (str): String timestamp.

    Returns:
        datetime: Datetime object.
    """
    return datetime.fromisoformat(str).replace(tzinfo=timezone.utc)


def datetime_utc(year, month, day, hour, minute):
    """Returns a datetime object in UTC timezone

    Args:
        year (int): eg. 2021
        month (int): between 1-12
        day (int): between 1-7
        hour (int): between 0-23
        minute (int): between 0-59

    Returns:
        datetime
    """
    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)


def next_url_fix(next_url):
    """A temporary solution to make cursor-based pagination work 
    with next URLs. This can ignored after OpenSea fixes the next URL.
    As of 2022-02-17 the cursor-based pagination does not work 
    without fixing the URL first.

    Args:
        url_not_working (str): the `next` value from the OpenSea response
    Returns:
        url (str): next URL that uses the *old* base url
    """
    working_url = "http://api.opensea.io/api/v1/"
    return working_url + next_url.split('/v1/')[-1]
