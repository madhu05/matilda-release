from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from matilda_release.api.v2.model.model import application

from datetime import datetime

def create_application(args):
    ap = models.Application()
    ap.app_id = args.get('app_id')
    ap.owner = args.get('owner')
    ap.create_dt = datetime.now()
    ap.status = args.get('status')
    ap.project_id = args.get('project_id')
    resp = db_api.create_application(ap)
    return resp


def get_applications(application_id=None, project_id=None):
    ap_list = db_api.get_applications(application_id, project_id)
    print('application list {}'.format(ap_list))
    resp = []
    for item in ap_list:
        item = item.to_dict()
        item['name'] = item['app_id'];
        for key in application:
            if key not in item.keys():
                item[key] = None
        resp.append(item)
    print("ap_list {}".format(ap_list))
    return resp
