import logging

from matilda_release.db.sqlalchemy.models import Milestone, MilestoneTypeCd
from werkzeug.exceptions import BadRequest

from datetime import datetime

from matilda_release.db import api as db_api

log = logging.getLogger(__name__)
debug = False

def get_milestone(milestone_id=None, release_id=None, filters=None):
    mls_info = db_api.get_milestone(milestone_id=milestone_id, release_id=release_id, filters=filters)
    log.debug('Milestone ID {}, Milestone Info {}'.format(milestone_id, mls_info))
    print ('release db data {}'.format(mls_info))
    return mls_info

def create_milestone(release_id=None, args=None):
    if release_id is None:
        raise BadRequest('release id is mandatory for creating milestone')

    mls_info = Milestone()
    mls_info.release_id = release_id
    # mls_info.milestone_type_cd = args.get('milestone_type_cd')
    mls_info.milestone_status_cd = args.get('milestone_status_cd')
    mls_info.milestone_description = args.get('milestone_description')
    mls_info.start_dt = datetime.strptime(args.get('start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    mls_info.end_dt = datetime.strptime(args.get('end_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    mls_info.percent_complete = args.get('percent_complete')
    if mls_info.percent_complete is not None:
        if not (mls_info.percent_complete > 0 and mls_info.percent_complete<=1):
            raise BadRequest('percent cannot be greater than 100 or less than 0')
    resp_milestone = db_api.create_milestone(args=mls_info)
    resp_milestone['start_dt'] = datetime.strftime(resp_milestone.get('start_dt'),
                                                   '%Y-%m-%dT%H:%M:%S.%fZ') if resp_milestone.get(
        'start_dt') is not None else None
    resp_milestone['end_dt'] = datetime.strftime(resp_milestone.get('end_dt'),
                                                 '%Y-%m-%dT%H:%M:%S.%fZ') if resp_milestone.get(
        'end_dt') is not None else None
    return resp_milestone

def update_milestone(release_id=None, milestone_id=None, args=None):
    print(release_id, milestone_id, args)
    mls_info = Milestone()
    mls_info.release_id = release_id
    mls_info.milestone_id = milestone_id
    mls_info.milestone_status_cd = args.get('milestone_status_cd')
    mls_info.milestone_description = args.get('milestone_description')
    mls_info.start_dt = datetime.strptime(args.get('start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    mls_info.end_dt = datetime.strptime(args.get('end_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    mls_info.percent_complete = args.get('percent_complete')
    if mls_info.percent_complete is not None:
        if not (mls_info.percent_complete > 0 and mls_info.percent_complete<=1):
            raise BadRequest('percent cannot be greater than 100 or less than 0')
    db_api.update_milestone(milestone_id=milestone_id, data=mls_info)
    resp = get_milestone(release_id=release_id, milestone_id=milestone_id)
    if isinstance(resp, list) and len(resp) > 0:
        resp = resp[0]
    resp['start_dt'] = datetime.strftime(resp.get('start_dt'), '%Y-%m-%dT%H:%M:%S.%fZ') if resp.get(
        'start_dt') is not None else None
    resp['end_dt'] = datetime.strftime(resp.get('end_dt'), '%Y-%m-%dT%H:%M:%S.%fZ') if resp.get(
        'end_dt') is not None else None
    return resp

def delete_milestone(release_id=None,milestone_id=None):
    return db_api.delete_milestone(release_id=release_id, milestone_id=milestone_id)


def get_milestone_type(release_type_cd=None, milestone_type_cd=None):
    milestone_type = db_api.get_milestone_type(release_type_cd=release_type_cd, milestone_type_cd=milestone_type_cd)
    return milestone_type


def create_milestone_type(release_type_cd=None, args=None):
    if release_type_cd is None:
        raise BadRequest('release_type_cd is mandatory for creating milestone type')
    mls_type_info = MilestoneTypeCd()
    mls_type_info.release_type_cd = release_type_cd
    mls_type_info.milestone_type_description = args.get('milestone_type_description')

    resp = db_api.create_milestone_type(args=mls_type_info)
    return resp

def update_milestone_type(release_type_cd=None, milestone_type_cd=None, args=None):
    mls_type_info = MilestoneTypeCd()
    mls_type_info.release_type_cd = release_type_cd
    mls_type_info.milestone_type_cd = milestone_type_cd
    mls_type_info.milestone_type_description = args.get('milestone_type_description')
    db_api.update_milestone_type(milestone_type_cd=milestone_type_cd, data=mls_type_info)
    resp = get_milestone_type(milestone_type_cd=milestone_type_cd)
    if isinstance(resp, list) and len(resp) > 0:
        resp = resp[0]
    return resp

def delete_milestone_type(release_type_cd=None,milestone_type_cd=None):
    return db_api.delete_milestone_type(release_type_cd=release_type_cd, milestone_type_cd=milestone_type_cd)

def get_milestone_status_cd(milestone_status_cd=None):
    milestone_status_cd = db_api.get_milestone_status(milestone_status_cd=milestone_status_cd, filters=None)
    return milestone_status_cd