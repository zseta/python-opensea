from datetime import datetime, timezone

def export_file(content, file_name):
    with open(file_name, 'wb') as f:
        f.write(content)
        
def str_to_datetime_utc(str):
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