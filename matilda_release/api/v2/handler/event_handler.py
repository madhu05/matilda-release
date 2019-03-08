from matilda_release.db import api as db_api
from matilda_release.util import event_types


def get_events(event_id=None, event_type=None, source_type=None, source_id=None, status=None):
    filters = {
        'event_id': event_id,
        'event_type': event_type,
        'source_type': source_type,
        'source_id': source_id,
        'status': status
    }
    resp = db_api.get_event(filters=filters)
    return resp


def post_events(event_list):
    resp = []
    for event in event_list:
        resp.append(db_api.create_event(event))
    return resp

def update_task(task_id, status, args):
    pass