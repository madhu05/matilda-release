import logging

from matilda_release.db.sqlalchemy.models import ReleasePlan
from datetime import datetime
from matilda_release.db import api as db_api

log = logging.getLogger(__name__)
debug = False


def get_release_plan(release_plan_id=None, release_type_cd=None, filters=None):
    release_plan_info = db_api.get_release_plan(release_plan_id=release_plan_id, release_type_cd=release_type_cd,
                                                filters=filters)
    print('release_plan info get call:{}'.format(release_plan_info))
    response = list()
    for release_plan in release_plan_info:
        temp_release_plan_detail = dict()
        temp_release_plan_detail_with_color = release_plan._asdict()
        temp_release_plan_detail.update(temp_release_plan_detail_with_color.get('ReleasePlan', {}))
        temp_release_plan_detail['color_pref'] = temp_release_plan_detail_with_color.get('color_pref')
        response.append(temp_release_plan_detail)
        return response

def create_release_plan(args=None):
    release_plan_info = ReleasePlan()
    release_plan_info.release_type_cd = args.get('release_type_cd')
    release_plan_info.release_plan_name = args.get('release_plan_name')
    release_plan_info.release_plan_description = args.get('release_plan_description')
    release_plan_info.release_owner = args.get('release_owner')
    release_plan_info.create_dt = datetime.now()
    release_plan_info.release_dt = datetime.strptime(args.get('release_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    resp_release_plan = db_api.create_release_plan(args=release_plan_info)

    final_resp = get_release_plan(release_plan_id=resp_release_plan.get('release_plan_id'))
    print('data is',final_resp)
    return final_resp


def update_release_plan(release_plan_id=None, args=None):
    release_plan_info = ReleasePlan()
    release_plan_info.release_plan_id = release_plan_id
    release_plan_info.release_type_cd = args.get('release_type_cd')
    release_plan_info.release_plan_name = args.get('release_plan_name')
    release_plan_info.release_plan_description = args.get('release_plan_description')
    release_plan_info.release_owner = args.get('release_owner')
    try:
        release_plan_info.create_dt = datetime.strptime(args.get('create_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        release_plan_info.create_dt = args.get('create_dt')

    release_plan_info.release_dt = datetime.strptime(args.get('release_dt'), '%Y-%m-%dT%H:%M:%S.%fZ')

    db_api.update_release_plan(release_plan_id=release_plan_id, args=release_plan_info)
    resp_release_plan = get_release_plan(release_plan_id=release_plan_id)
    if resp_release_plan is not None and type(resp_release_plan) is list:
        resp_release_plan = resp_release_plan[0]
        return resp_release_plan


def delete_release_plan(release_plan_id):
    return db_api.delete_release_plan(release_plan_id=release_plan_id)
