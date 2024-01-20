import datetime


def create_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
